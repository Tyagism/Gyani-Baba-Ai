"""
GEO (Generative Engine Optimization) Auditor Module.
Analyzes document content against GEO best practices to score
and recommend improvements for AI search visibility.
"""

from __future__ import annotations
import json
from models.schemas import GEOAuditResult, GEOAuditReport
from utils.gemini_client import GeminiClient
from utils.helpers import clean_json_response


GEO_AUDIT_SYSTEM = """You are a Generative Engine Optimization (GEO) expert.
GEO is the practice of optimizing content to be cited, mentioned, and recommended 
by AI search engines (ChatGPT, Google AI Overviews, Perplexity, etc.).

You audit content across these dimensions:
1. Content Authority (E-E-A-T) — credentials, citations, data sourcing, expertise signals
2. Structural Clarity — headings, lists, tables, logical organization for LLM parsing
3. Factual Accuracy — properly sourced stats, current data, verifiable claims
4. Citation Worthiness — does this content deserve to be cited by AI engines?
5. Entity Coverage — are key entities clearly defined with context?
6. Conversational Readiness — does the content directly answer questions?

For each dimension, provide:
- A score (0-100)
- Specific findings (what you observed)
- Actionable recommendations (what to improve)"""

# Categories with their icons
AUDIT_CATEGORIES = [
    ("Content Authority (E-E-A-T)", "🏆"),
    ("Structural Clarity", "🏗️"),
    ("Factual Accuracy", "✅"),
    ("Citation Worthiness", "📎"),
    ("Entity Coverage", "🔍"),
    ("Conversational Readiness", "💬"),
]


def run_geo_audit(
    document_text: str,
    client: GeminiClient,
    fact_check_score: float = -1,
) -> GEOAuditReport:
    """
    Run a comprehensive GEO audit on the document content.
    
    Args:
        document_text: Full document text.
        client: Initialized Gemini client.
        fact_check_score: Trust score from fact-checking (-1 if not available).
    
    Returns:
        GEOAuditReport with scores and recommendations.
    """
    categories_str = "\n".join([f"- {name}" for name, _ in AUDIT_CATEGORIES])

    fact_check_note = ""
    if fact_check_score >= 0:
        fact_check_note = f"\nNOTE: This document has a fact-check trust score of {fact_check_score}%. Factor this into the Factual Accuracy score."

    prompt = f"""Perform a comprehensive GEO (Generative Engine Optimization) audit on 
the following document content.

Audit across these 6 categories:
{categories_str}
{fact_check_note}

DOCUMENT CONTENT (first 5000 chars):
{document_text[:5000]}

For EACH category, provide:
- score (0-100): how well does the content perform?
- findings (list of 2-4 specific observations)
- recommendations (list of 2-4 actionable improvements)

Also provide 3-5 PRIORITY ACTIONS — the most impactful things to do first.

Respond with JSON:
{{
    "categories": [
        {{
            "name": "Content Authority (E-E-A-T)",
            "score": 75,
            "findings": ["finding 1", "finding 2"],
            "recommendations": ["recommendation 1", "recommendation 2"]
        }}
    ],
    "priority_actions": [
        "Most impactful action 1",
        "Most impactful action 2"
    ]
}}"""

    try:
        response = client.generate(
            prompt=prompt,
            system_instruction=GEO_AUDIT_SYSTEM,
            temperature=0.3,
            use_grounding=True,
        )

        cleaned = clean_json_response(response)
        data = json.loads(cleaned)

        categories = []
        for cat_data in data.get("categories", []):
            name = cat_data.get("name", "Unknown")
            # Find matching icon
            icon = "📊"
            for cat_name, cat_icon in AUDIT_CATEGORIES:
                if cat_name.lower() in name.lower() or name.lower() in cat_name.lower():
                    icon = cat_icon
                    break

            categories.append(GEOAuditResult(
                category=name,
                score=float(cat_data.get("score", 50)),
                findings=cat_data.get("findings", []),
                recommendations=cat_data.get("recommendations", []),
                icon=icon,
            ))

        # Ensure we have all 6 categories
        existing_names = {c.category.lower() for c in categories}
        for cat_name, cat_icon in AUDIT_CATEGORIES:
            if not any(cat_name.lower() in en for en in existing_names):
                categories.append(GEOAuditResult(
                    category=cat_name,
                    score=50,
                    findings=["Insufficient data for detailed analysis."],
                    recommendations=["Provide more content for a thorough audit."],
                    icon=cat_icon,
                ))

        report = GEOAuditReport(
            categories=categories[:6],
            priority_actions=data.get("priority_actions", []),
        )
        report.compute_overall()
        return report

    except Exception as e:
        # Return default report on failure
        default_cats = [
            GEOAuditResult(
                category=name,
                score=50,
                findings=["Analysis could not be completed."],
                recommendations=["Re-run the audit with a clearer document."],
                icon=icon,
            )
            for name, icon in AUDIT_CATEGORIES
        ]
        report = GEOAuditReport(
            categories=default_cats,
            priority_actions=[f"Audit failed: {str(e)[:100]}. Please retry."],
        )
        report.compute_overall()
        return report
