"""
Gemini API client wrapper with singleton pattern and configuration.
Handles client initialization, model selection, and grounding setup.
"""

from __future__ import annotations
import os
import time
import json
import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv(override=True)
# ─── Constants ───────────────────────────────────────────────────────────────

DEFAULT_MODEL = "gemini-2.5-flash"
MAX_RETRIES = 3
RETRY_DELAY = 15  # seconds (longer backoff for 429 Resource Exhausted)


class GeminiClient:
    """Wrapper around the Google GenAI client with convenience methods."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY", "")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found. Set it in your .env file.")
        self.client = genai.Client(api_key=self.api_key)
        self.model = DEFAULT_MODEL

    def generate(
        self,
        prompt: str,
        system_instruction: str = "",
        temperature: float = 0.3,
        use_grounding: bool = False,
        response_schema: type | None = None,
    ) -> str:
        """Generate content with optional grounding and structured output."""
        tools = []
        if use_grounding:
            tools.append(types.Tool(google_search=types.GoogleSearch()))

        config_kwargs = {
            "temperature": temperature,
        }
        if system_instruction:
            config_kwargs["system_instruction"] = system_instruction
        if tools:
            config_kwargs["tools"] = tools
        if response_schema and not use_grounding:
            config_kwargs["response_mime_type"] = "application/json"
            config_kwargs["response_schema"] = response_schema

        config = types.GenerateContentConfig(**config_kwargs)

        for attempt in range(MAX_RETRIES):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=config,
                )
                return response.text or ""
            except Exception as e:
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY * (attempt + 1))
                else:
                    raise RuntimeError(f"Gemini API failed after {MAX_RETRIES} retries: {e}")

    def generate_with_grounding_metadata(
        self,
        prompt: str,
        system_instruction: str = "",
        temperature: float = 0.1,
    ) -> tuple[str, list[str], list[str]]:
        """Generate with grounding and return (text, source_urls, search_queries)."""
        tools = [types.Tool(google_search=types.GoogleSearch())]

        config_kwargs = {
            "temperature": temperature,
            "tools": tools,
        }
        if system_instruction:
            config_kwargs["system_instruction"] = system_instruction

        config = types.GenerateContentConfig(**config_kwargs)

        for attempt in range(MAX_RETRIES):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=config,
                )

                text = response.text or ""
                sources = []
                queries = []

                # Extract grounding metadata
                if response.candidates:
                    candidate = response.candidates[0]
                    grounding = getattr(candidate, "grounding_metadata", None)
                    if grounding:
                        # Extract search queries
                        web_queries = getattr(grounding, "web_search_queries", None)
                        if web_queries:
                            queries = list(web_queries)

                        # Extract grounding chunks / sources
                        chunks = getattr(grounding, "grounding_chunks", None)
                        if chunks:
                            for chunk in chunks:
                                web = getattr(chunk, "web", None)
                                if web:
                                    uri = getattr(web, "uri", None)
                                    if uri:
                                        sources.append(uri)

                        # Fallback: grounding supports
                        supports = getattr(grounding, "grounding_supports", None)
                        if supports and not sources:
                            for support in supports:
                                refs = getattr(support, "grounding_chunk_indices", [])
                                # These refer back to grounding_chunks

                return text, list(set(sources)), queries

            except Exception as e:
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY * (attempt + 1))
                else:
                    raise RuntimeError(f"Gemini API failed after {MAX_RETRIES} retries: {e}")

    def upload_file(self, file_bytes: bytes, filename: str, mime_type: str = "application/pdf"):
        """Upload a file to Gemini Files API for large document processing."""
        import tempfile
        import os

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name

        try:
            uploaded = self.client.files.upload(
                file=tmp_path,
                config=types.UploadFileConfig(
                    mime_type=mime_type,
                    display_name=filename,
                ),
            )
            return uploaded
        finally:
            os.unlink(tmp_path)

    def generate_with_file(
        self,
        uploaded_file,
        prompt: str,
        system_instruction: str = "",
        temperature: float = 0.2,
    ) -> str:
        """Generate content using an uploaded file reference."""
        config_kwargs = {
            "temperature": temperature,
        }
        if system_instruction:
            config_kwargs["system_instruction"] = system_instruction

        config = types.GenerateContentConfig(**config_kwargs)

        for attempt in range(MAX_RETRIES):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=[
                        types.Part.from_uri(
                            file_uri=uploaded_file.uri,
                            mime_type=uploaded_file.mime_type,
                        ),
                        prompt,
                    ],
                    config=config,
                )
                return response.text or ""
            except Exception as e:
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY * (attempt + 1))
                else:
                    raise RuntimeError(f"Gemini API failed after {MAX_RETRIES} retries: {e}")


def get_gemini_client() -> GeminiClient:
    """Get or create a singleton Gemini client (cached by Streamlit)."""
    return GeminiClient()
