"""
Shared utility functions for formatting, colors, and UI helpers.
"""

from __future__ import annotations
from models.schemas import VerificationStatus, ClaimType


def format_file_size(size_bytes: int) -> str:
    """Format bytes into human-readable size string."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"


def get_status_color(status: VerificationStatus) -> str:
    """Get the CSS color for a verification status."""
    colors = {
        VerificationStatus.VERIFIED: "#10B981",     # Emerald
        VerificationStatus.INACCURATE: "#F59E0B",   # Amber
        VerificationStatus.FALSE: "#EF4444",         # Red
        VerificationStatus.UNVERIFIABLE: "#6B7280",  # Gray
    }
    return colors.get(status, "#6B7280")


def get_status_icon(status: VerificationStatus) -> str:
    """Get the emoji icon for a verification status."""
    icons = {
        VerificationStatus.VERIFIED: "✅",
        VerificationStatus.INACCURATE: "⚠️",
        VerificationStatus.FALSE: "❌",
        VerificationStatus.UNVERIFIABLE: "❓",
    }
    return icons.get(status, "❓")


def get_claim_type_icon(claim_type: ClaimType) -> str:
    """Get the emoji icon for a claim type."""
    icons = {
        ClaimType.STATISTIC: "📊",
        ClaimType.DATE: "📅",
        ClaimType.FINANCIAL: "💰",
        ClaimType.TECHNICAL: "🔧",
        ClaimType.CONTEXTUAL: "📑",
        ClaimType.GENERAL: "📰",
    }
    return icons.get(claim_type, "📝")


def get_trust_score_color(score: float) -> str:
    """Get color for trust score gauge."""
    if score >= 70:
        return "#10B981"  # Green
    elif score >= 40:
        return "#F59E0B"  # Amber
    else:
        return "#EF4444"  # Red


def get_trust_score_label(score: float) -> str:
    """Get label for trust score."""
    if score >= 80:
        return "Highly Trustworthy"
    elif score >= 60:
        return "Mostly Reliable"
    elif score >= 40:
        return "Needs Verification"
    elif score >= 20:
        return "Unreliable"
    else:
        return "Highly Suspect"


def truncate_text(text: str, max_length: int = 200) -> str:
    """Truncate text with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(" ", 1)[0] + "..."


def clean_json_response(text: str) -> str:
    """Clean Gemini response to extract JSON content."""
    text = text.strip()
    # Remove markdown code fences if present
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()
