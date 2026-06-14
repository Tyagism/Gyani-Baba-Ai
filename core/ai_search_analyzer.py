"""
AI Search Analyzer Module.
Simulates AI search visibility analysis by querying Gemini
to evaluate how well a brand/product is represented in AI search results.
"""

from __future__ import annotations
import json
import time
from models.schemas import AISearchResult, AISearchReport
from utils.gemini_client import GeminiClient
from utils.helpers import clean_json_response


AI_SEARCH_SYSTEM_PROMPT = """You are an AI Search Visibility Analyst. You analyze how brands, 
products, and content appear in AI-generated search results.

When given a brand/topic and search prompts, you must:
1. Search the web and analyze current information about this brand/topic
2. Determine if the brand would likely be mentioned in AI-generated answers
3. Identify competitors that would appear instead
4. Assess the sentiment of how this brand is discussed online
5. Evaluate citation potential — would AI engines cite this brand's content?

Respond with a JSON object:
{
    "brand_mentioned": true/false,
    "citation_found": true/false,
    "position": 0-5 (estimated rank in AI response, 0=not found),
    "sentiment": "positive|neutral|negative",
    "competitor_mentions": ["competitor1", "competitor2"],
    "response_snippet": "brief excerpt of what an AI would say"
}"""


def analyze_ai_search(
    document_text: str,
    client: GeminiClient,
    brand_name: str = "",
    num_prompts: int = 8,
) -> AISearchReport:
    """
    Analyze AI search visibility for the content/brand in the document.
    
    Args:
        document_text: Full document text.
        client: Initialized Gemini client.
        brand_name: Brand/entity name to track. Auto-detected if empty.
        num_prompts: Number of test prompts to generate and analyze.
    
    Returns:
        AISearchReport with visibility metrics.
    """
    # Step 1: Extract brand/entity name and key topics if not provided
    if not brand_name:
        brand_name = _extract_brand_name(document_text, client)

    # Step 2: Generate realistic search prompts
    prompts = _generate_search_prompts(document_text, brand_name, client, num_prompts)

    # Step 3: Analyze each prompt for brand visibility
    results = []
    engines = ["Google AI Overview", "ChatGPT", "Perplexity", "Gemini"]

    for prompt_text in prompts:
        # Simulate across different "engines" by varying the query angle
        engine = engines[len(results) % len(engines)]
        try:
            result = _analyze_single_prompt(prompt_text, brand_name, engine, client)
            results.append(result)
        except Exception:
            results.append(AISearchResult(
                prompt=prompt_text,
                ai_engine=engine,
                brand_mentioned=False,
                response_snippet="Analysis failed",
            ))
        time.sleep(0.5)

    # Step 4: Compute aggregate metrics
    report = AISearchReport(brand_name=brand_name, results=results)
    report.total_prompts_tested = len(results)

    if results:
        report.mention_rate = round(
            sum(1 for r in results if r.brand_mentioned) / len(results) * 100, 1
        )
        report.citation_rate = round(
            sum(1 for r in results if r.citation_found) / len(results) * 100, 1
        )

        # Aggregate competitors
        all_competitors = []
        for r in results:
            all_competitors.extend(r.competitor_mentions)
        # Count and sort
        comp_counts = {}
        for c in all_competitors:
            comp_counts[c] = comp_counts.get(c, 0) + 1
        report.top_competitors = sorted(comp_counts, key=comp_counts.get, reverse=True)[:5]

        # Sentiment
        sentiment_map = {"positive": 1, "neutral": 0, "negative": -1}
        scores = [sentiment_map.get(r.sentiment, 0) for r in results]
        report.avg_sentiment_score = round(sum(scores) / len(scores), 2) if scores else 0

    return report


def _extract_brand_name(document_text: str, client: GeminiClient) -> str:
    """Auto-detect the primary brand/entity from the document."""
    prompt = f"""From the following document text, identify the PRIMARY brand, company, 
product, or entity that this document is about. Return ONLY the name, nothing else.

DOCUMENT (first 2000 chars):
{document_text[:2000]}"""

    response = client.generate(prompt=prompt, temperature=0.1)
    return response.strip().strip('"').strip("'")[:100]


def _generate_search_prompts(
    document_text: str,
    brand_name: str,
    client: GeminiClient,
    num_prompts: int,
) -> list[str]:
    """Generate realistic AI search prompts related to the document's content."""
    prompt = f"""Generate {num_prompts} realistic search prompts that users would type into 
AI search engines (ChatGPT, Google, Perplexity) related to the following content.

Brand/Entity: {brand_name}
Document Content (first 3000 chars):
{document_text[:3000]}

The prompts should be:
- Natural language questions users would actually ask
- Mix of informational, comparison, and recommendation queries
- Related to the brand's industry/niche
- Include some that should mention {brand_name} and some generic industry queries

Return ONLY a JSON array of strings:
["prompt1", "prompt2", ...]"""

    try:
        response = client.generate(prompt=prompt, temperature=0.4)
        cleaned = clean_json_response(response)
        prompts = json.loads(cleaned)
        if isinstance(prompts, list):
            return [str(p) for p in prompts[:num_prompts]]
    except Exception:
        pass

    # Fallback prompts
    return [
        f"What is {brand_name}?",
        f"Best alternatives to {brand_name}",
        f"Is {brand_name} good?",
        f"{brand_name} review",
    ]


def _analyze_single_prompt(
    prompt_text: str,
    brand_name: str,
    engine: str,
    client: GeminiClient,
) -> AISearchResult:
    """Analyze a single prompt for brand visibility in AI search."""

    analysis_prompt = f"""Imagine you are the AI engine "{engine}" answering the following user query.
Search the web for current data and generate a realistic answer.

USER QUERY: "{prompt_text}"

Now analyze your response for the brand "{brand_name}":

Respond with JSON:
{{
    "brand_mentioned": true/false (would {brand_name} appear in this answer?),
    "citation_found": true/false (would the answer cite/link to {brand_name}'s website?),
    "position": 0-5 (where would {brand_name} appear? 1=first, 0=not at all),
    "sentiment": "positive|neutral|negative",
    "competitor_mentions": ["list", "of", "competitors", "that", "would", "appear"],
    "response_snippet": "a 2-3 sentence excerpt of what the AI would say"
}}"""

    response_text, sources, _ = client.generate_with_grounding_metadata(
        prompt=analysis_prompt,
        system_instruction=AI_SEARCH_SYSTEM_PROMPT,
        temperature=0.3,
    )

    try:
        cleaned = clean_json_response(response_text)
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        data = {
            "brand_mentioned": brand_name.lower() in response_text.lower(),
            "citation_found": False,
            "position": 0,
            "sentiment": "neutral",
            "competitor_mentions": [],
            "response_snippet": response_text[:200],
        }

    return AISearchResult(
        prompt=prompt_text,
        ai_engine=engine,
        brand_mentioned=data.get("brand_mentioned", False),
        citation_found=data.get("citation_found", False),
        position=int(data.get("position", 0)),
        sentiment=data.get("sentiment", "neutral"),
        competitor_mentions=data.get("competitor_mentions", [])[:5],
        response_snippet=data.get("response_snippet", ""),
    )
