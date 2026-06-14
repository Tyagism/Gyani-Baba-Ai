"""
PDF Processing Module.
Extracts text content from uploaded PDFs using Gemini's native PDF understanding,
with PyPDF2 as a fallback (with user notification popup).
"""

from __future__ import annotations
import streamlit as st
from PyPDF2 import PdfReader
import io

from models.schemas import DocumentContent
from utils.gemini_client import GeminiClient


def process_pdf(
    file_bytes: bytes,
    filename: str,
    file_size_mb: float,
    client: GeminiClient,
) -> DocumentContent:
    """
    Extract text from a PDF using Gemini first, PyPDF2 as fallback.
    Shows a popup warning if falling back to PyPDF2.
    """
    try:
        return _extract_with_gemini(file_bytes, filename, file_size_mb, client)
    except Exception as gemini_error:
        # Show popup notification about fallback
        st.warning(
            f"⚠️ **Gemini PDF processing failed:** {str(gemini_error)[:200]}\n\n"
            f"Falling back to **PyPDF2** for basic text extraction. "
            f"Some tables, charts, and complex formatting may not be captured accurately.",
            icon="⚠️",
        )
        st.toast("Using PyPDF2 fallback for PDF extraction...", icon="📄")

        try:
            return _extract_with_pypdf2(file_bytes, filename, file_size_mb)
        except Exception as pypdf_error:
            raise RuntimeError(
                f"Both extraction methods failed.\n"
                f"Gemini: {gemini_error}\n"
                f"PyPDF2: {pypdf_error}"
            )


def _extract_with_gemini(
    file_bytes: bytes,
    filename: str,
    file_size_mb: float,
    client: GeminiClient,
) -> DocumentContent:
    """Extract text using Gemini's native PDF understanding."""

    # Upload file to Gemini Files API
    uploaded_file = client.upload_file(file_bytes, filename)

    system_prompt = """You are a precise document text extractor. Extract ALL text content
from this PDF document. Maintain the structure including:
- Headings and subheadings
- Paragraphs
- Lists and bullet points
- Table data (convert to readable text format)
- Footnotes and references
- Any numerical data, statistics, dates, and figures

For each page, prefix the content with [PAGE X] where X is the page number.
Be thorough — do NOT skip or summarize any content. Extract everything verbatim."""

    response_text = client.generate_with_file(
        uploaded_file=uploaded_file,
        prompt="Extract all text content from this PDF document, page by page. Include every piece of text, number, date, and data point.",
        system_instruction=system_prompt,
        temperature=0.1,
    )

    # Parse page-wise content
    page_texts = _parse_page_markers(response_text)
    total_pages = len(page_texts) if page_texts else 1

    if not page_texts:
        page_texts = {1: response_text}

    return DocumentContent(
        filename=filename,
        total_pages=total_pages,
        full_text=response_text,
        page_texts=page_texts,
        file_size_mb=file_size_mb,
        extraction_method="gemini",
    )


def _extract_with_pypdf2(
    file_bytes: bytes,
    filename: str,
    file_size_mb: float,
) -> DocumentContent:
    """Fallback extraction using PyPDF2."""
    reader = PdfReader(io.BytesIO(file_bytes))
    page_texts = {}
    all_text_parts = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        page_num = i + 1
        page_texts[page_num] = text
        all_text_parts.append(f"[PAGE {page_num}]\n{text}")

    full_text = "\n\n".join(all_text_parts)
    total_pages = len(reader.pages)

    return DocumentContent(
        filename=filename,
        total_pages=total_pages,
        full_text=full_text,
        page_texts=page_texts,
        file_size_mb=file_size_mb,
        extraction_method="pypdf2",
    )


def _parse_page_markers(text: str) -> dict[int, str]:
    """Parse [PAGE X] markers from extracted text into a page dictionary."""
    import re

    page_texts = {}
    # Split by [PAGE N] markers
    pattern = r'\[PAGE\s+(\d+)\]'
    parts = re.split(pattern, text)

    if len(parts) < 2:
        # No page markers found
        return {}

    # parts alternates: [pre-text, page_num, content, page_num, content, ...]
    for i in range(1, len(parts) - 1, 2):
        try:
            page_num = int(parts[i])
            content = parts[i + 1].strip()
            page_texts[page_num] = content
        except (ValueError, IndexError):
            continue

    return page_texts
