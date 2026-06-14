"""
Page 5: About — Project information and how it works.
"""

import streamlit as st
from utils.navigation import render_theme_toggle, render_go_back_button
from pathlib import Path

# ─── Page Config ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="About | Gyani-Baba",
    page_icon="ℹ️",
    layout="wide",
)
render_theme_toggle()
render_go_back_button()

# Load CSS
css_path = Path(__file__).parent.parent / "assets" / "styles.css"
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ─── Header ──────────────────────────────────────────────────────────────────

st.markdown("""
<div class="app-header animate-fade-in">
    <h1>ℹ️ About Gyani-Baba</h1>
    <p>The Truth Layer for AI-Powered Fact-Checking & Search Intelligence</p>
</div>
""", unsafe_allow_html=True)

# ─── What is Gyani-Baba ─────────────────────────────────────────────────────

st.markdown("""
<div class="glass-card animate-fade-in">
    <h3 style="color: #F1F5F9; margin-top: 0;">🧠 What is Gyani-Baba?</h3>
    <p style="color: #94A3B8; line-height: 1.8; font-size: 0.95rem;">
        Gyani-Baba is an AI-powered <strong>Fact-Checking Agent</strong> and 
        <strong>AI Search Intelligence Platform</strong>. It reads your PDF documents, 
        extracts every verifiable claim, and cross-references them against live web data using 
        Google's Gemini AI with Search Grounding.
    </p>
    <p style="color: #94A3B8; line-height: 1.8; font-size: 0.95rem;">
        Beyond fact-checking, it provides <strong style="color: #8B5CF6;">AI Search Analytics</strong> — 
        analyzing how your content appears in AI-generated search results across ChatGPT, Google AI Overviews, 
        Perplexity, and more.
    </p>
</div>
""", unsafe_allow_html=True)

# ─── How It Works ────────────────────────────────────────────────────────────

st.markdown('<div class="section-header">⚙️ How It Works</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="glass-card" style="text-align: center; min-height: 280px;">
        <div style="
            font-size: 2.5rem;
            margin-bottom: 0.8rem;
            background: linear-gradient(135deg, #3B82F6, #7C3AED);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        ">📄</div>
        <h4 style="color: #F1F5F9; margin-bottom: 0.5rem;">1. Extract</h4>
        <p style="color: #94A3B8; font-size: 0.85rem; line-height: 1.6;">
            Upload a PDF and Gemini AI extracts every verifiable claim — 
            statistics, dates, financial figures, technical specs, and contextual assertions.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-card" style="text-align: center; min-height: 280px;">
        <div style="
            font-size: 2.5rem;
            margin-bottom: 0.8rem;
            background: linear-gradient(135deg, #7C3AED, #10B981);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        ">🔍</div>
        <h4 style="color: #F1F5F9; margin-bottom: 0.5rem;">2. Verify</h4>
        <p style="color: #94A3B8; font-size: 0.85rem; line-height: 1.6;">
            Each claim is verified against live web data using Google Search Grounding — 
            the same technology powering Google's AI Overviews.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="glass-card" style="text-align: center; min-height: 280px;">
        <div style="
            font-size: 2.5rem;
            margin-bottom: 0.8rem;
            background: linear-gradient(135deg, #10B981, #F59E0B);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        ">📊</div>
        <h4 style="color: #F1F5F9; margin-bottom: 0.5rem;">3. Report</h4>
        <p style="color: #94A3B8; font-size: 0.85rem; line-height: 1.6;">
            Claims are flagged as Verified ✅, Inaccurate ⚠️, or False ❌ — 
            with correct values, explanations, and source links.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ─── Features ────────────────────────────────────────────────────────────────

st.markdown('<div class="glass-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">🚀 Features</div>', unsafe_allow_html=True)

features = [
    ("📄 PDF Fact-Checking", "Upload any PDF and get a claim-by-claim fact-check report with trust scores"),
    ("🔍 AI Search Analytics", "Track how your brand appears in ChatGPT, Perplexity, Google AI Overviews"),
    ("💡 Prompt Research", "Discover what questions users ask AI about your topic"),
    ("📊 GEO Optimization", "Audit content for Generative Engine Optimization with actionable recommendations"),
    ("🌐 Live Web Grounding", "All verifications use real-time Google Search data — not cached or stale"),
    ("📥 Export Reports", "Download complete fact-check reports as JSON for further analysis"),
]

col_a, col_b = st.columns(2)
for i, (title, desc) in enumerate(features):
    with (col_a if i % 2 == 0 else col_b):
        st.markdown(f"""
        <div class="glass-card" style="padding: 1rem 1.2rem; margin-bottom: 0.5rem;">
            <h4 style="color: #F1F5F9; margin: 0 0 0.3rem 0; font-size: 0.95rem;">{title}</h4>
            <p style="color: #94A3B8; font-size: 0.8rem; margin: 0;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)



# ─── Tech Stack ──────────────────────────────────────────────────────────────

st.markdown('<div class="glass-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">🛠️ Technology Stack</div>', unsafe_allow_html=True)

tech = [
    ("Streamlit", "Frontend framework"),
    ("Google Gemini 2.5 Flash", "AI model for extraction & verification"),
    ("Google Search Grounding", "Live web data verification"),
    ("Plotly", "Interactive analytics charts"),
    ("Pydantic", "Data validation & schemas"),
    ("PyPDF2", "Fallback PDF parser"),
]

cols = st.columns(3)
for i, (name, desc) in enumerate(tech):
    with cols[i % 3]:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: 1rem;">
            <div style="color: #8B5CF6; font-weight: 700; font-size: 0.9rem;">{name}</div>
            <div style="color: #94A3B8; font-size: 0.75rem; margin-top: 0.2rem;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

# ─── Footer ──────────────────────────────────────────────────────────────────

st.markdown("""
<div class="app-footer">
    <a href="https://github.com/Tyagism">Gyani-Baba v1.0 — Built with ❤️ using Google Gemini AI API<br>
    © 2026 Gyani-Baba by Harshit Tyagi | Fact-Check Agent & AI Search Intelligence</a>
</div>
""", unsafe_allow_html=True)
