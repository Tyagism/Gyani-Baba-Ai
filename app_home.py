"""
Gyani-Baba — Fact-Check Agent & AI Search Intelligence Platform

Main entry point. Configures the Streamlit app with multi-page navigation,
glassmorphism theming, and global session state.
"""

import streamlit as st
from utils.navigation import render_theme_toggle, render_go_back_button
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ─── Page Config (must be first Streamlit call) ─────────────────────────────

st.set_page_config(
    page_title="Gyani-Baba | Fact-Check & AI Search Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Load Custom CSS ────────────────────────────────────────────────────────

def load_css():
    """Inject the glassmorphism CSS design system."""
    css_path = Path(__file__).parent / "assets" / "styles.css"
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()
render_theme_toggle()

# ─── Session State Initialization ────────────────────────────────────────────

def init_session_state():
    """Initialize all session state variables."""
    defaults = {
        "document_content": None,
        "extracted_claims": None,
        "fact_check_report": None,
        "ai_search_report": None,
        "prompt_research": None,
        "geo_audit_report": None,
        "uploaded_file_name": None,
        "processing_stage": None,  # "extracting", "verifying", "complete"
        "pdf_size_limit_mb": 100,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ─── Sidebar ────────────────────────────────────────────────────────────────

with st.sidebar:
    render_go_back_button()
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <div style="font-size: 2.5rem; margin-bottom: 0.3rem;">🧠</div>
        <h2 style="
            background: linear-gradient(135deg, #7C3AED, #3B82F6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 1.5rem;
            font-weight: 800;
            margin: 0;
        ">Gyani-Baba</h2>
        <p style="color: #94A3B8; font-size: 0.8rem; margin-top: 0.2rem;">
            Truth Layer & AI Search Intelligence
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Show processing status
    if st.session_state.uploaded_file_name:
        st.markdown(f"""
        <div style="
            background: rgba(124, 58, 237, 0.1);
            border: 1px solid rgba(124, 58, 237, 0.2);
            border-radius: 10px;
            padding: 0.8rem;
            margin-bottom: 1rem;
        ">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em;">
                Current Document
            </div>
            <div style="color: #F1F5F9; font-weight: 600; font-size: 0.9rem; margin-top: 0.3rem;">
                📄 {st.session_state.uploaded_file_name}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # PDF Size Limit Slider
    st.markdown("##### ⚙️ Settings")
    st.session_state.pdf_size_limit_mb = st.slider(
        "PDF Size Limit (MB)",
        min_value=10,
        max_value=500,
        value=st.session_state.pdf_size_limit_mb,
        step=10,
        help="Adjust if you need to upload files larger than 100MB",
    )

    st.markdown("---")

    # Navigation status indicators
    has_doc = st.session_state.document_content is not None
    has_fc = st.session_state.fact_check_report is not None
    has_ai = st.session_state.ai_search_report is not None
    has_pr = st.session_state.prompt_research is not None
    has_geo = st.session_state.geo_audit_report is not None

    st.markdown("##### 📊 Analysis Status")
    status_items = [
        ("PDF Uploaded", has_doc),
        ("Fact-Check", has_fc),
        ("AI Search", has_ai),
        ("Prompts", has_pr),
        ("GEO Audit", has_geo),
    ]
    for label, done in status_items:
        icon = "✅" if done else "⬜"
        st.markdown(f"{icon} {label}")

    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #64748B; font-size: 0.7rem; padding: 1rem 0;">
        Built with ❤️ using Gemini AI<br>
        © 2026 Gyani-Baba
    </div>
    """, unsafe_allow_html=True)


# ─── Main Content Area ──────────────────────────────────────────────────────

# Header
st.markdown("""
<div class="app-header animate-fade-in">
    <h1>🧠 Gyani-Baba</h1>
    <p>Building the Truth Layer — AI-Powered Fact-Checking & Search Intelligence</p>
</div>
""", unsafe_allow_html=True)

# Quick feature navigation
if not st.session_state.document_content:
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <p style="color: #94A3B8; font-size: 1.1rem; margin-bottom: 2rem;">
            Upload a PDF to get started. Gyani-Baba will extract claims, verify them against live web data, 
            and provide AI search optimization insights.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Feature cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <a href="/Upload_&_Analyze" target="_self" style="text-decoration: none;">
            <div class="glass-card" style="text-align: center; min-height: 200px; cursor: pointer; transition: transform 0.2s;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📄</div>
                <h4 style="color: #F1F5F9; font-size: 1rem; margin-bottom: 0.5rem;">Upload & Analyze</h4>
                <p style="color: #94A3B8; font-size: 0.8rem;">
                    Upload PDFs and extract verifiable claims automatically
                </p>
            </div>
        </a>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <a href="/AI_Search_Analytics" target="_self" style="text-decoration: none;">
            <div class="glass-card" style="text-align: center; min-height: 200px; cursor: pointer; transition: transform 0.2s;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔍</div>
                <h4 style="color: #F1F5F9; font-size: 1rem; margin-bottom: 0.5rem;">AI Search Analytics</h4>
                <p style="color: #94A3B8; font-size: 0.8rem;">
                    Track brand visibility across AI search engines
                </p>
            </div>
        </a>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <a href="/Prompt_Research" target="_self" style="text-decoration: none;">
            <div class="glass-card" style="text-align: center; min-height: 200px; cursor: pointer; transition: transform 0.2s;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">💡</div>
                <h4 style="color: #F1F5F9; font-size: 1rem; margin-bottom: 0.5rem;">Prompt Research</h4>
                <p style="color: #94A3B8; font-size: 0.8rem;">
                    Discover what users ask AI about your topic
                </p>
            </div>
        </a>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <a href="/GEO_Optimization" target="_self" style="text-decoration: none;">
            <div class="glass-card" style="text-align: center; min-height: 200px; cursor: pointer; transition: transform 0.2s;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📊</div>
                <h4 style="color: #F1F5F9; font-size: 1rem; margin-bottom: 0.5rem;">GEO Optimization</h4>
                <p style="color: #94A3B8; font-size: 0.8rem;">
                    Audit and optimize content for AI search ranking
                </p>
            </div>
        </a>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.info("👈 **Navigate to 'Upload & Analyze'** from the sidebar to get started!")

else:
    # Document loaded — show summary
    doc = st.session_state.document_content
    report = st.session_state.fact_check_report

    st.markdown(f"""
    <div class="glass-card animate-fade-in">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h3 style="color: #F1F5F9; margin: 0;">📄 {doc.filename}</h3>
                <p style="color: #94A3B8; font-size: 0.85rem; margin-top: 0.3rem;">
                    {doc.total_pages} pages • {doc.file_size_mb:.1f} MB • Extracted via {doc.extraction_method}
                </p>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 0.75rem; color: #94A3B8;">TRUST SCORE</div>
                <div style="font-size: 2rem; font-weight: 800; color: {'#10B981' if report and report.overall_trust_score >= 70 else '#F59E0B' if report and report.overall_trust_score >= 40 else '#EF4444' if report else '#94A3B8'};">
                    {f"{report.overall_trust_score:.0f}%" if report else "—"}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.info("👈 Use the sidebar pages to explore detailed analysis results.")

# Footer
st.markdown("""
<div class="app-footer">
    Gyani-Baba v1.0 — Fact-Check Agent & AI Search Intelligence Platform<br>
    Powered by Google Gemini AI with Live Web Grounding
</div>
""", unsafe_allow_html=True)
