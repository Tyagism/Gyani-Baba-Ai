"""
Pydantic data models for the Gyani-Baba fact-checking pipeline.
All structured data flows through these schemas.
"""

from __future__ import annotations
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


# ─── Enums ───────────────────────────────────────────────────────────────────

class ClaimType(str, Enum):
    """Classification of extracted claims."""
    STATISTIC = "statistic"
    DATE = "date"
    FINANCIAL = "financial"
    TECHNICAL = "technical"
    CONTEXTUAL = "contextual"
    GENERAL = "general"


class VerificationStatus(str, Enum):
    """Fact-check verdict for a claim."""
    VERIFIED = "Verified"
    INACCURATE = "Inaccurate"
    FALSE = "False"
    UNVERIFIABLE = "Unverifiable"


# ─── Document Models ────────────────────────────────────────────────────────

class DocumentContent(BaseModel):
    """Parsed content from an uploaded PDF."""
    filename: str
    total_pages: int
    full_text: str
    page_texts: dict[int, str] = Field(default_factory=dict)
    file_size_mb: float = 0.0
    extraction_method: str = "gemini"  # "gemini" or "pypdf2"


# ─── Claim Extraction Models ────────────────────────────────────────────────

class ExtractedClaim(BaseModel):
    """A single verifiable claim extracted from a document."""
    id: int = 0
    claim_text: str = Field(description="The exact claim as stated in the document")
    claim_type: ClaimType = Field(description="Category of the claim")
    source_page: int = Field(default=1, description="Page number where claim appears")
    source_context: str = Field(default="", description="Surrounding text for context")
    confidence: float = Field(default=0.8, ge=0.0, le=1.0, description="Extraction confidence 0-1")


# ─── Verification Models ────────────────────────────────────────────────────

class VerificationResult(BaseModel):
    """Result of fact-checking a single claim against live web data."""
    claim: ExtractedClaim
    status: VerificationStatus
    correct_value: Optional[str] = Field(default=None, description="The correct/current value if claim is wrong")
    explanation: str = Field(default="", description="Why this verdict was reached")
    sources: list[str] = Field(default_factory=list, description="Source URLs used for verification")
    search_queries_used: list[str] = Field(default_factory=list, description="Search queries Gemini performed")


class FactCheckReport(BaseModel):
    """Complete fact-check report for an uploaded document."""
    document_name: str
    total_claims: int = 0
    verified_count: int = 0
    inaccurate_count: int = 0
    false_count: int = 0
    unverifiable_count: int = 0
    results: list[VerificationResult] = Field(default_factory=list)
    overall_trust_score: float = Field(default=0.0, ge=0.0, le=100.0)
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

    def compute_scores(self):
        """Recalculate counts and trust score from results."""
        self.total_claims = len(self.results)
        self.verified_count = sum(1 for r in self.results if r.status == VerificationStatus.VERIFIED)
        self.inaccurate_count = sum(1 for r in self.results if r.status == VerificationStatus.INACCURATE)
        self.false_count = sum(1 for r in self.results if r.status == VerificationStatus.FALSE)
        self.unverifiable_count = sum(1 for r in self.results if r.status == VerificationStatus.UNVERIFIABLE)
        if self.total_claims > 0:
            self.overall_trust_score = round((self.verified_count / self.total_claims) * 100, 1)
        else:
            self.overall_trust_score = 0.0


# ─── AI Search Analytics Models ─────────────────────────────────────────────

class AISearchResult(BaseModel):
    """Result from simulating an AI search query."""
    prompt: str
    ai_engine: str = "Google AI Overview"
    brand_mentioned: bool = False
    citation_found: bool = False
    position: int = Field(default=0, description="Position in AI answer, 0 = not found")
    sentiment: str = "neutral"  # positive, neutral, negative
    competitor_mentions: list[str] = Field(default_factory=list)
    response_snippet: str = ""


class AISearchReport(BaseModel):
    """Aggregate AI search visibility report."""
    brand_name: str
    results: list[AISearchResult] = Field(default_factory=list)
    total_prompts_tested: int = 0
    mention_rate: float = 0.0
    citation_rate: float = 0.0
    avg_sentiment_score: float = 0.0
    top_competitors: list[str] = Field(default_factory=list)


# ─── Prompt Research Models ─────────────────────────────────────────────────

class PromptResearchResult(BaseModel):
    """Discovered prompts users might ask AI about the document's topic."""
    seed_topic: str
    discovered_prompts: list[str] = Field(default_factory=list)
    prompt_intents: dict[str, str] = Field(default_factory=dict, description="prompt -> intent mapping")
    relevance_scores: dict[str, float] = Field(default_factory=dict, description="prompt -> score mapping")
    content_gaps: list[str] = Field(default_factory=list, description="Questions the document doesn't answer")


# ─── GEO Audit Models ───────────────────────────────────────────────────────

class GEOAuditResult(BaseModel):
    """Score and recommendations for one GEO audit category."""
    category: str
    score: float = Field(default=0.0, ge=0.0, le=100.0)
    findings: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    icon: str = "📊"


class GEOAuditReport(BaseModel):
    """Complete GEO optimization audit."""
    overall_score: float = 0.0
    categories: list[GEOAuditResult] = Field(default_factory=list)
    priority_actions: list[str] = Field(default_factory=list)

    def compute_overall(self):
        """Calculate weighted overall score."""
        if self.categories:
            self.overall_score = round(
                sum(c.score for c in self.categories) / len(self.categories), 1
            )
