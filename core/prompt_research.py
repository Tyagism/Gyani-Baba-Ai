"""
Prompt Research Module.
Discovers relevant user prompts that AI search engines receive,
and analyzes how well the document's content answers them.
"""

from __future__ import annotations
import json
from models.schemas import PromptResearchResult
from utils.gemini_client import GeminiClient
from utils.helpers import clean_json_response


PROMPT_RESEARCH_SYSTEM = """You are a Prompt Research & Discovery specialist.
You help content creators understand what questions and prompts users ask AI assistants
about their industry, brand, and topics. This is critical for AI Search Optimization (GEO).

Your analysis should cover:
1. Discovery of natural-language prompts users ask AI about this topic
2. Classification of prompt intent (informational, transactional, navigational, comparison)
3. Relevance scoring (how well does the document answer each prompt? 0.0-1.0)
4. Content gap identification (what important questions does the document NOT answer?)"""


def research_prompts(
    document_text: str,
    client: GeminiClient,
    num_prompts: int = 15,
) -> PromptResearchResult:
    """
    Research what prompts users ask AI about the document's topics.
    
    Args:
        document_text: Full document text.
        client: Initialized Gemini client.
        num_prompts: Number of prompts to discover.
    
    Returns:
        PromptResearchResult with discovered prompts, intents, and gaps.
    """
    # Step 1: Extract seed topics
    seed_topic = _extract_seed_topic(document_text, client)

    # Step 2: Discover prompts
    prompt = f"""Based on the topic "{seed_topic}" and the following document content,
discover {num_prompts} realistic prompts/questions that real users would ask AI assistants
(ChatGPT, Google, Perplexity, Claude) about this topic.

DOCUMENT (first 4000 chars):
{document_text[:4000]}

For each prompt, provide:
- The natural-language prompt itself
- The intent category: "informational", "transactional", "navigational", or "comparison"
- A relevance score (0.0-1.0): how well does the given document answer this prompt?
  (1.0 = perfectly answers, 0.0 = doesn't address at all)

Also identify 5 important CONTENT GAPS — questions users would ask that the document 
does NOT answer well.

Respond with JSON:
{{
    "prompts": [
        {{
            "text": "prompt text",
            "intent": "informational|transactional|navigational|comparison",
            "relevance": 0.8
        }}
    ],
    "content_gaps": [
        "Important question the document doesn't answer"
    ]
}}"""

    try:
        response = client.generate(
            prompt=prompt,
            system_instruction=PROMPT_RESEARCH_SYSTEM,
            temperature=0.4,
            use_grounding=True,
        )

        cleaned = clean_json_response(response)
        data = json.loads(cleaned)

        prompts_data = data.get("prompts", [])
        discovered = [p["text"] for p in prompts_data if "text" in p]
        intents = {p["text"]: p.get("intent", "informational") for p in prompts_data if "text" in p}
        scores = {p["text"]: float(p.get("relevance", 0.5)) for p in prompts_data if "text" in p}
        gaps = data.get("content_gaps", [])

        return PromptResearchResult(
            seed_topic=seed_topic,
            discovered_prompts=discovered,
            prompt_intents=intents,
            relevance_scores=scores,
            content_gaps=gaps,
        )

    except Exception:
        return PromptResearchResult(
            seed_topic=seed_topic,
            discovered_prompts=[
                f"What is {seed_topic}?",
                f"Best {seed_topic} tools",
                f"{seed_topic} comparison",
            ],
            content_gaps=["Unable to analyze content gaps due to processing error."],
        )


def _extract_seed_topic(document_text: str, client: GeminiClient) -> str:
    """Extract the primary topic/subject from the document."""
    prompt = f"""What is the main topic or subject of the following document?
Return ONLY a short phrase (2-6 words), nothing else.

DOCUMENT (first 1500 chars):
{document_text[:1500]}"""

    response = client.generate(prompt=prompt, temperature=0.1)
    return response.strip().strip('"').strip("'")[:100]
