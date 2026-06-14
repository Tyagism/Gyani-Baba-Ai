"""
Page 1: Upload & Analyze — PDF upload, claim extraction, and fact-check report.
The core page of Gyani-Baba.
"""

import streamlit as st
from utils.navigation import render_theme_toggle, render_go_back_button
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ─── Page Config ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Upload & Analyze | Gyani-Baba",
    page_icon="📄",
    layout="wide",
)
render_theme_toggle()
render_go_back_button()

# Load CSS
css_path = Path(__file__).parent.parent / "assets" / "styles.css"
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ─── Imports ─────────────────────────────────────────────────────────────────

from core.pdf_processor import process_pdf
from core.claim_extractor import extract_claims
from core.fact_verifier import verify_claims
from utils.gemini_client import get_gemini_client
from utils.animations import inject_animation_css, render_scanner, render_alternating_animations, inject_custom_fact_check_button
from utils.helpers import (
    get_status_color,
    get_status_icon,
    get_claim_type_icon,
    get_trust_score_color,
    get_trust_score_label,
    format_file_size,
)
from models.schemas import VerificationStatus

# ─── Session State Defaults ─────────────────────────────────────────────────

for key in ["document_content", "extracted_claims", "fact_check_report",
            "uploaded_file_name", "processing_stage", "pdf_size_limit_mb"]:
    if key not in st.session_state:
        st.session_state[key] = None if key != "pdf_size_limit_mb" else 100

def _run_analysis(uploaded_file):
    """Run the full extraction and verification pipeline."""
    try:
        client = get_gemini_client()
    except Exception as e:
        st.error(f"❌ Failed to initialize Gemini client: {e}\\n\\nMake sure your `GOOGLE_API_KEY` is set in the `.env` file.")
        return

    file_bytes = uploaded_file.getvalue()
    file_size_mb = len(file_bytes) / (1024 * 1024)

    # Progress tracking
    progress_bar = st.progress(0, text="Initializing...")
    
    try:
        with st.status("⚙️ Analyzing Document...", expanded=True) as status:
            anim_container = st.empty()
            
            # Stage 1: PDF Extraction
            st.session_state.processing_stage = "extracting"
            anim_container.markdown(render_scanner(), unsafe_allow_html=True)
            
            progress_bar.progress(5, text="📄 Extracting text from PDF...")
            st.write("🔄 **Stage 1/3:** Processing PDF with Gemini AI...")

            doc_content = process_pdf(
                file_bytes=file_bytes,
                filename=uploaded_file.name,
                file_size_mb=file_size_mb,
                client=client,
            )
            st.session_state.document_content = doc_content
            st.session_state.uploaded_file_name = uploaded_file.name

            progress_bar.progress(25, text="✅ PDF extracted successfully!")
            st.write("✅ PDF text and metadata extracted successfully.")

            # Stage 2: Claim Extraction
            st.session_state.processing_stage = "extracting_claims"
            anim_container.markdown(render_alternating_animations(), unsafe_allow_html=True)
            
            progress_bar.progress(30, text="🔍 Extracting verifiable claims...")
            st.write("🔄 **Stage 2/3:** Identifying claims, stats, dates, and facts...")

            claims = extract_claims(
                document_text=doc_content.full_text,
                client=client,
            )
            st.session_state.extracted_claims = claims

            progress_bar.progress(45, text=f"✅ Found {len(claims)} verifiable claims!")
            st.write(f"✅ Extracted **{len(claims)}** verifiable claims from the document.")

            # Stage 3: Fact Verification
            st.session_state.processing_stage = "verifying"
            st.write(f"🔄 **Stage 3/3:** Verifying {len(claims)} claims against live web data using Google Search grounding...")

            def update_progress(current, total, text):
                pct = 45 + int((current / max(total, 1)) * 50)
                progress_bar.progress(min(pct, 95), text=text)

            report = verify_claims(
                claims=claims,
                document_name=uploaded_file.name,
                client=client,
                progress_callback=update_progress,
            )
            st.session_state.fact_check_report = report

            progress_bar.progress(100, text="✅ Analysis complete!")
            st.write("🎉 **Fact-check complete!** Generating report...")
            anim_container.empty() # Clear the animation
            status.update(label="✅ Analysis Complete!", state="complete", expanded=False)
            
        st.session_state.processing_stage = "complete"

        st.rerun()

    except Exception as e:
        progress_bar.empty()
        st.error(f"❌ Analysis failed: {str(e)}")
        st.session_state.processing_stage = None


# ─── Header ──────────────────────────────────────────────────────────────────

st.markdown("""
<div class="app-header animate-fade-in">
    <h1>📄 Upload & Analyze</h1>
    <p>Upload a PDF — we'll extract claims and verify them against live web data</p>
</div>
""", unsafe_allow_html=True)

# Inject the animation CSS globally
inject_animation_css()

# ─── Upload Section ─────────────────────────────────────────────────────────

if st.session_state.fact_check_report is None:

    uploaded_file = st.file_uploader(
        f"Upload PDF (up to {st.session_state.get('pdf_size_limit_mb', 100)}MB)",
        type=["pdf"],
        key="pdf_uploader",
    )

    if uploaded_file is not None:
        file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
        limit = st.session_state.get("pdf_size_limit_mb", 100)

        if file_size_mb > limit:
            st.error(
                f"❌ File size ({file_size_mb:.1f}MB) exceeds the current limit ({limit}MB). "
                f"Adjust the PDF size limit slider in the sidebar settings."
            )
        else:
            st.markdown(f"""
            <div class="glass-card animate-fade-in">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4 style="color: #F1F5F9; margin: 0;">📄 {uploaded_file.name}</h4>
                        <p style="color: #94A3B8; font-size: 0.85rem; margin-top: 0.3rem;">
                            {format_file_size(len(uploaded_file.getvalue()))}
                        </p>
                    </div>
                    <div style="color: #10B981; font-weight: 600;">Ready to analyze</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            inject_custom_fact_check_button()
            if st.button("🚀 Start Fact-Check Analysis", use_container_width=True):
                _run_analysis(uploaded_file)


def _domain_from_url(url: str) -> str:
    """Extract domain name from a URL for display."""
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        domain = parsed.netloc
        if domain.startswith("www."):
            domain = domain[4:]
        return domain[:30]
    except Exception:
        return url[:30]


# ─── Results Display ────────────────────────────────────────────────────────


if st.session_state.fact_check_report is not None:
    report = st.session_state.fact_check_report
    doc = st.session_state.document_content

    # ── Extracted Document Content ──
    with st.expander("📄 View Extracted Document Content", expanded=False):
        st.markdown("**Raw Text Extracted by AI:**")
        st.text_area("Document Text", doc.full_text, height=200, disabled=True, label_visibility="collapsed")

    # ── Trust Score Header ──
    score = report.overall_trust_score
    score_color = get_trust_score_color(score)
    score_label = get_trust_score_label(score)

    st.markdown(f"""
    <div class="trust-gauge animate-fade-in" style="margin-bottom: 1.5rem;">
        <div style="font-size: 0.8rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5rem;">
            Overall Trust Score
        </div>
        <div class="score-value" style="color: {score_color};">
            {score:.0f}%
        </div>
        <div class="score-label">{score_label}</div>
        <div style="margin-top: 1rem;">
            <div class="score-bar-container" style="height: 10px; max-width: 300px; margin: 0 auto;">
                <div class="score-bar-fill" style="width: {score}%; background: linear-gradient(90deg, {score_color}, {score_color}88);"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI Cards ──
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(f"""
        <div class="stat-card primary">
            <div class="stat-value">{report.total_claims}</div>
            <div class="stat-label">Total Claims</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stat-card verified">
            <div class="stat-value">{report.verified_count}</div>
            <div class="stat-label">✅ Verified</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="stat-card inaccurate">
            <div class="stat-value">{report.inaccurate_count}</div>
            <div class="stat-label">⚠️ Inaccurate</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="stat-card false">
            <div class="stat-value">{report.false_count}</div>
            <div class="stat-label">❌ False</div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
        <div class="stat-card info">
            <div class="stat-value">{report.unverifiable_count}</div>
            <div class="stat-label">❓ Unverifiable</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="glass-divider"></div>', unsafe_allow_html=True)

    # ── Filter Tabs ──
    tab_all, tab_verified, tab_inaccurate, tab_false, tab_unverifiable = st.tabs([
        f"All ({report.total_claims})",
        f"✅ Verified ({report.verified_count})",
        f"⚠️ Inaccurate ({report.inaccurate_count})",
        f"❌ False ({report.false_count})",
        f"❓ Unverifiable ({report.unverifiable_count})",
    ])

    def render_claim_results(results):
        """Render a list of verification results."""
        if not results:
            st.info("No claims in this category.")
            return

        for i, result in enumerate(results):
            claim = result.claim
            status = result.status
            icon = get_status_icon(status)
            color = get_status_color(status)
            type_icon = get_claim_type_icon(claim.claim_type)
            status_class = status.value.lower()

            with st.expander(
                f"{icon} **Claim #{claim.id}** — {claim.claim_text[:80]}{'...' if len(claim.claim_text) > 80 else ''}",
                expanded=(status in [VerificationStatus.FALSE, VerificationStatus.INACCURATE]),
            ):
                # Claim details
                st.markdown(f"""
                <div class="claim-card {status_class}">
                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.8rem;">
                        <div>
                            <span class="status-badge {status_class}">{icon} {status.value}</span>
                            <span style="margin-left: 0.5rem; color: #94A3B8; font-size: 0.8rem;">
                                {type_icon} {claim.claim_type.value} • Page {claim.source_page}
                            </span>
                        </div>
                    </div>
                    <div style="color: #F1F5F9; font-size: 0.95rem; margin-bottom: 0.8rem; line-height: 1.5;">
                        "{claim.claim_text}"
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Correct value (if different)
                if result.correct_value:
                    st.markdown(f"""
                    <div style="
                        background: rgba(16, 185, 129, 0.1);
                        border: 1px solid rgba(16, 185, 129, 0.2);
                        border-radius: 10px;
                        padding: 0.8rem 1rem;
                        margin-bottom: 0.8rem;
                    ">
                        <div style="font-size: 0.75rem; color: #10B981; text-transform: uppercase; font-weight: 600; letter-spacing: 0.05em;">
                            ✅ Correct Value
                        </div>
                        <div style="color: #F1F5F9; margin-top: 0.3rem;">{result.correct_value}</div>
                    </div>
                    """, unsafe_allow_html=True)

                # Explanation
                st.markdown(f"""
                <div style="color: #94A3B8; font-size: 0.85rem; margin-bottom: 0.8rem; line-height: 1.6;">
                    <strong style="color: #F1F5F9;">Explanation:</strong> {result.explanation}
                </div>
                """, unsafe_allow_html=True)

                # Sources
                if result.sources:
                    sources_html = " ".join([
                        f'<a href="{s}" target="_blank" class="source-link">🔗 {_domain_from_url(s)}</a>'
                        for s in result.sources[:5]
                    ])
                    st.markdown(f"""
                    <div style="margin-top: 0.5rem;">
                        <span style="color: #94A3B8; font-size: 0.75rem; font-weight: 600;">Sources: </span>
                        {sources_html}
                    </div>
                    """, unsafe_allow_html=True)

    with tab_all:
        render_claim_results(report.results)

    with tab_verified:
        render_claim_results([r for r in report.results if r.status == VerificationStatus.VERIFIED])

    with tab_inaccurate:
        render_claim_results([r for r in report.results if r.status == VerificationStatus.INACCURATE])

    with tab_false:
        render_claim_results([r for r in report.results if r.status == VerificationStatus.FALSE])

    with tab_unverifiable:
        render_claim_results([r for r in report.results if r.status == VerificationStatus.UNVERIFIABLE])

    # ── Export ──
    st.markdown('<div class="glass-divider"></div>', unsafe_allow_html=True)

    col_export1, col_export2, col_export3 = st.columns([1, 1, 2])
    with col_export1:
        json_data = report.model_dump_json(indent=2)
        st.download_button(
            label="📥 Export Report (JSON)",
            data=json_data.encode("utf-8"),
            file_name=f"fact_check_report.json",
            mime="application/json",
            key="export_json_btn"
        )
    with col_export2:
        if st.button("🔄 Analyze New Document"):
            for key in ["document_content", "extracted_claims", "fact_check_report",
                        "ai_search_report", "prompt_research", "geo_audit_report",
                        "uploaded_file_name", "processing_stage"]:
                st.session_state[key] = None
            st.rerun()


