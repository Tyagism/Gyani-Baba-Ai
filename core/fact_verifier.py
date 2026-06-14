"""
Fact Verification Module.
Uses Gemini with Google Search Grounding to verify claims against live web data.
This is the core "Truth Layer" engine.
"""

from __future__ import annotations
import json
import time
import streamlit as st
from models.schemas import (
    ExtractedClaim,
    VerificationResult,
    VerificationStatus,
    FactCheckReport,
)
from utils.gemini_client import GeminiClient
from utils.helpers import clean_json_response


VERIFICATION_SYSTEM_PROMPT = """You are an expert forensic fact-checker with access to live web search. 
Your job is to verify claims against CURRENT, AUTHORITATIVE web data.

For the given claim, you MUST:
1. Search the web for the most recent, authoritative data on this topic
2. Compare the claim's specific numbers, dates, and facts against what you find
3. Make a definitive judgment

CLASSIFICATION RULES:
- **VERIFIED**: The claim matches current authoritative data (exact or very close match)
- **INACCURATE**: The claim contains outdated data, slightly wrong numbers, or partial truths. The spirit may be correct but specific values are wrong.
- **FALSE**: The claim is demonstrably wrong, fabricated, contradicted by evidence, or there is strong evidence against it
- **UNVERIFIABLE**: Cannot find reliable sources to confirm or deny

CRITICAL: You must respond with ONLY a valid JSON object with these fields:
{
    "status": "Verified|Inaccurate|False|Unverifiable",
    "correct_value": "the actual correct current value/fact if different from claim, or null if verified",
    "explanation": "detailed explanation of your verification process and findings",
    "key_sources": ["list of key source descriptions"]
}

Be PRECISE and STRICT. If a number is even slightly off, mark as INACCURATE and provide the correct figure.
If a date is wrong, mark as FALSE or INACCURATE depending on severity.
Always provide the CORRECT, CURRENT value when available."""


def verify_claims(
    claims: list[ExtractedClaim],
    document_name: str,
    client: GeminiClient,
    progress_callback=None,
) -> FactCheckReport:
    """
    Verify a list of claims against live web data using Gemini with Google Search Grounding.

    Args:
        claims: List of extracted claims to verify.
        document_name: Name of the source document.
        client: Initialized Gemini client.
        progress_callback: Optional callable(current, total, status_text) for progress updates.

    Returns:
        FactCheckReport with all verification results.
    """
    report = FactCheckReport(document_name=document_name)
    results = []

    total = len(claims)
    for i, claim in enumerate(claims):
        if progress_callback:
            progress_callback(i, total, f"Verifying claim {i + 1}/{total}: {claim.claim_text[:60]}...")

        try:
            result = _verify_single_claim(claim, client)
            results.append(result)
        except Exception as e:
            # On failure, mark as unverifiable rather than crashing
            results.append(
                VerificationResult(
                    claim=claim,
                    status=VerificationStatus.UNVERIFIABLE,
                    explanation=f"Verification failed: {str(e)[:200]}",
                    sources=[],
                    search_queries_used=[],
                )
            )

        # Rate limiting: wait 4.2 seconds between API calls to stay under 15 Requests/Minute (Free Tier)
        if i < total - 1:
            time.sleep(4.2)

    report.results = results
    report.compute_scores()

    if progress_callback:
        progress_callback(total, total, "✅ Verification complete!")

    return report


def _verify_single_claim(
    claim: ExtractedClaim,
    client: GeminiClient,
) -> VerificationResult:
    """Verify a single claim using Gemini with Google Search grounding."""

    verification_prompt = f"""CLAIM TO VERIFY:
"{claim.claim_text}"

CLAIM TYPE: {claim.claim_type.value}
CONTEXT FROM DOCUMENT: {claim.source_context}

Search the web and verify whether this claim is accurate based on current, authoritative data. 
Respond with a JSON object containing: status, correct_value, explanation, key_sources."""

    # Use grounding to get web-verified response + source URLs
    response_text, source_urls, search_queries = client.generate_with_grounding_metadata(
        prompt=verification_prompt,
        system_instruction=VERIFICATION_SYSTEM_PROMPT,
        temperature=0.1,
    )

    # Parse the response
    try:
        cleaned = clean_json_response(response_text)
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        # Try to extract verdict from unstructured response
        data = _parse_unstructured_response(response_text)

    # Map status
    status_str = data.get("status", "Unverifiable")
    status = _map_status(status_str)

    # Build source list: combine grounding URLs with any mentioned in response
    all_sources = list(set(source_urls + data.get("key_sources", [])))

    return VerificationResult(
        claim=claim,
        status=status,
        correct_value=data.get("correct_value"),
        explanation=data.get("explanation", "No explanation provided."),
        sources=all_sources[:10],  # Cap at 10 sources
        search_queries_used=search_queries,
    )


def _map_status(status_str: str) -> VerificationStatus:
    """Map a string status to VerificationStatus enum."""
    status_lower = status_str.lower().strip()
    if "verified" in status_lower or "true" == status_lower or "correct" in status_lower:
        return VerificationStatus.VERIFIED
    elif "inaccurate" in status_lower or "outdated" in status_lower or "partially" in status_lower:
        return VerificationStatus.INACCURATE
    elif "false" in status_lower or "wrong" in status_lower or "fabricated" in status_lower:
        return VerificationStatus.FALSE
    else:
        return VerificationStatus.UNVERIFIABLE


def _parse_unstructured_response(text: str) -> dict:
    """Attempt to parse verdict from non-JSON response."""
    text_lower = text.lower()

    # Determine status from keywords
    if any(w in text_lower for w in ["false", "incorrect", "wrong", "fabricated", "no evidence"]):
        status = "False"
    elif any(w in text_lower for w in ["inaccurate", "outdated", "partially", "slightly off"]):
        status = "Inaccurate"
    elif any(w in text_lower for w in ["verified", "confirmed", "accurate", "correct"]):
        status = "Verified"
    else:
        status = "Unverifiable"

    return {
        "status": status,
        "correct_value": None,
        "explanation": text[:500],
        "key_sources": [],
    }
