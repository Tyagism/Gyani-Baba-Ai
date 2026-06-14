"""
Claim Extraction Module.
Uses Gemini to forensically extract all verifiable claims from document text.
Includes contextual claims about the document's topic and data.
"""

from __future__ import annotations
import json
from models.schemas import ExtractedClaim, ClaimType
from utils.gemini_client import GeminiClient
from utils.helpers import clean_json_response


EXTRACTION_SYSTEM_PROMPT = """You are a forensic fact-checker and document analyst. Your job is to extract EVERY verifiable claim from the given document text.

You must identify and extract claims in these categories:

1. **STATISTIC** — percentages, growth rates, market share, survey results, population data
2. **DATE** — founding dates, event dates, timelines, deadlines, historical dates
3. **FINANCIAL** — revenue, valuations, funding amounts, pricing, market cap, budgets
4. **TECHNICAL** — specifications, performance metrics, measurements, scientific data
5. **CONTEXTUAL** — claims about the document's own topic, subject matter expertise, industry context, relationships between entities described, cause-effect claims about the data presented
6. **GENERAL** — company info, personnel, locations, product names, organizational claims

CRITICAL RULES:
- Extract SPECIFIC, VERIFIABLE facts only — not opinions or subjective statements
- Include the EXACT numbers, dates, and values as stated in the document
- Note the page number where each claim appears (from [PAGE X] markers)
- Include surrounding context (1-2 sentences around the claim)
- Be EXHAUSTIVE — extract every single verifiable data point
- For CONTEXTUAL claims: extract claims about what the data means, relationships described between entities, and factual assertions about the topic itself
- Assign a confidence score (0.0-1.0) for how clearly the claim is stated

Respond with a JSON array of objects, each with these fields:
{
  "claim_text": "exact claim as stated",
  "claim_type": "statistic|date|financial|technical|contextual|general",
  "source_page": 1,
  "source_context": "surrounding text for context",
  "confidence": 0.9
}"""


def extract_claims(
    document_text: str,
    client: GeminiClient,
    max_claims: int = 500,
) -> list[ExtractedClaim]:
    """
    Extract verifiable claims from document text using Gemini.

    Args:
        document_text: Full text of the document with page markers.
        client: Initialized Gemini client.
        max_claims: Maximum number of claims to extract.

    Returns:
        List of ExtractedClaim objects.
    """

    # Truncate if extremely long (Gemini context window considerations)
    if len(document_text) > 100000:
        document_text = document_text[:100000] + "\n\n[DOCUMENT TRUNCATED DUE TO LENGTH]"

    prompt = f"""Analyze the following document and extract ALL verifiable claims. 
Return a JSON array of claim objects.

DOCUMENT TEXT:
---
{document_text}
---

Extract ALL verifiable claims. Focus on facts that can be verified against 
real-world data, especially statistics, dates, financial figures, technical specs, 
and contextual/topical assertions. Do not stop until all claims are extracted."""

    try:
        response_text = client.generate(
            prompt=prompt,
            system_instruction=EXTRACTION_SYSTEM_PROMPT,
            temperature=0.1,
        )

        # Parse JSON response
        cleaned = clean_json_response(response_text)
        claims_data = json.loads(cleaned)

        if not isinstance(claims_data, list):
            claims_data = [claims_data]

        claims = []
        for i, item in enumerate(claims_data[:max_claims]):
            try:
                claim_type_str = item.get("claim_type", "general").lower()
                claim_type = _map_claim_type(claim_type_str)

                claim = ExtractedClaim(
                    id=i + 1,
                    claim_text=item.get("claim_text", ""),
                    claim_type=claim_type,
                    source_page=int(item.get("source_page", 1)),
                    source_context=item.get("source_context", ""),
                    confidence=float(item.get("confidence", 0.8)),
                )
                if claim.claim_text.strip():
                    claims.append(claim)
            except Exception:
                continue

        return claims

    except json.JSONDecodeError:
        # If JSON parsing fails, try a simpler extraction
        return _fallback_extraction(response_text)
    except Exception as e:
        raise RuntimeError(f"Claim extraction failed: {e}")


def _map_claim_type(type_str: str) -> ClaimType:
    """Map a string claim type to the ClaimType enum."""
    mapping = {
        "statistic": ClaimType.STATISTIC,
        "statistics": ClaimType.STATISTIC,
        "stat": ClaimType.STATISTIC,
        "date": ClaimType.DATE,
        "dates": ClaimType.DATE,
        "financial": ClaimType.FINANCIAL,
        "finance": ClaimType.FINANCIAL,
        "technical": ClaimType.TECHNICAL,
        "tech": ClaimType.TECHNICAL,
        "contextual": ClaimType.CONTEXTUAL,
        "context": ClaimType.CONTEXTUAL,
        "general": ClaimType.GENERAL,
    }
    return mapping.get(type_str.lower(), ClaimType.GENERAL)


def _fallback_extraction(raw_text: str) -> list[ExtractedClaim]:
    """Simple fallback if JSON parsing of Gemini response fails."""
    claims = []
    lines = raw_text.strip().split("\n")

    for i, line in enumerate(lines):
        line = line.strip()
        if line and len(line) > 20 and not line.startswith("#"):
            # Remove bullet points and numbering
            clean_line = line.lstrip("•-*0123456789. ")
            if clean_line:
                claims.append(
                    ExtractedClaim(
                        id=i + 1,
                        claim_text=clean_line,
                        claim_type=ClaimType.GENERAL,
                        source_page=1,
                        source_context="",
                        confidence=0.5,
                    )
                )

    return claims[:30]
