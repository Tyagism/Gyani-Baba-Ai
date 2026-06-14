"""
Page 2: AI Search Analytics — Brand visibility dashboard.
"""

import streamlit as st
from utils.navigation import render_theme_toggle, render_go_back_button
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ─── Page Config ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="AI Search Analytics | Gyani-Baba",
    page_icon="🔍",
    layout="wide",
)
render_theme_toggle()
render_go_back_button()

# Load CSS
css_path = Path(__file__).parent.parent / "assets" / "styles.css"
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

from core.ai_search_analyzer import analyze_ai_search
from utils.gemini_client import get_gemini_client

# ─── Header ──────────────────────────────────────────────────────────────────

st.markdown("""
<div class="app-header animate-fade-in">
    <h1>🔍 AI Search Analytics</h1>
    <p>Track brand visibility across AI search engines</p>
</div>
""", unsafe_allow_html=True)

# ─── Check Prerequisites ────────────────────────────────────────────────────

if "document_content" not in st.session_state or st.session_state.document_content is None:
    st.markdown("""
    <div class="glass-card" style="text-align: center; padding: 3rem;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">📄</div>
        <h3 style="color: #F1F5F9;">No Document Uploaded</h3>
        <p style="color: #94A3B8;">Upload and analyze a PDF first from the "Upload & Analyze" page.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ─── Run Analysis ────────────────────────────────────────────────────────────

if "ai_search_report" not in st.session_state:
    st.session_state.ai_search_report = None

doc = st.session_state.document_content

# Brand name input
col_brand, col_btn = st.columns([3, 1])
with col_brand:
    brand_name = st.text_input(
        "Brand / Entity Name",
        value="",
        placeholder="Auto-detected if left empty",
        help="The brand or entity to track in AI search results",
    )
with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    run_analysis = st.button("🚀 Run AI Search Analysis", type="primary", use_container_width=True)

if run_analysis:
    try:
        client = get_gemini_client()
        with st.spinner("🔍 Analyzing AI search visibility... This may take 30-60 seconds."):
            report = analyze_ai_search(
                document_text=doc.full_text,
                client=client,
                brand_name=brand_name if brand_name else "",
                num_prompts=8,
            )
            st.session_state.ai_search_report = report
            st.rerun()
    except Exception as e:
        st.error(f"❌ Analysis failed: {e}")

# ─── Display Results ─────────────────────────────────────────────────────────

if st.session_state.ai_search_report is not None:
    report = st.session_state.ai_search_report

    # ── KPI Row ──
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="stat-card primary">
            <div class="stat-value">{report.brand_name}</div>
            <div class="stat-label">Brand Tracked</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        mention_color = "#10B981" if report.mention_rate >= 50 else "#F59E0B" if report.mention_rate >= 25 else "#EF4444"
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value" style="color: {mention_color};">{report.mention_rate:.0f}%</div>
            <div class="stat-label">Mention Rate</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        cite_color = "#10B981" if report.citation_rate >= 40 else "#F59E0B" if report.citation_rate >= 20 else "#EF4444"
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value" style="color: {cite_color};">{report.citation_rate:.0f}%</div>
            <div class="stat-label">Citation Rate</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        sent_label = "Positive" if report.avg_sentiment_score > 0.3 else "Negative" if report.avg_sentiment_score < -0.3 else "Neutral"
        sent_color = "#10B981" if report.avg_sentiment_score > 0.3 else "#EF4444" if report.avg_sentiment_score < -0.3 else "#F59E0B"
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value" style="color: {sent_color};">{sent_label}</div>
            <div class="stat-label">Avg Sentiment</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="glass-divider"></div>', unsafe_allow_html=True)

    # ── Charts Row ──
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown('<div class="section-header">📊 Visibility by AI Engine</div>', unsafe_allow_html=True)

        # Group by engine
        engine_data = {}
        for r in report.results:
            engine_data.setdefault(r.ai_engine, {"mentioned": 0, "total": 0})
            engine_data[r.ai_engine]["total"] += 1
            if r.brand_mentioned:
                engine_data[r.ai_engine]["mentioned"] += 1

        if engine_data:
            engines = list(engine_data.keys())
            rates = [
                (engine_data[e]["mentioned"] / engine_data[e]["total"] * 100) if engine_data[e]["total"] > 0 else 0
                for e in engines
            ]

            fig = go.Figure(go.Bar(
                x=rates,
                y=engines,
                orientation='h',
                marker=dict(
                    color=rates,
                    colorscale=[[0, '#EF4444'], [0.5, '#F59E0B'], [1, '#10B981']],
                    line=dict(width=0),
                ),
                text=[f"{r:.0f}%" for r in rates],
                textposition='outside',
                textfont=dict(color='#F1F5F9', size=12),
            ))
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=40, t=10, b=10),
                height=250,
                xaxis=dict(range=[0, 110], showgrid=False, showticklabels=False),
                yaxis=dict(showgrid=False),
                font=dict(family="Inter, sans-serif"),
            )
            st.plotly_chart(fig, use_container_width=True)

    with col_chart2:
        st.markdown('<div class="section-header">🏆 Top Competitors</div>', unsafe_allow_html=True)

        if report.top_competitors:
            # Count competitor mentions
            comp_counts = {}
            for r in report.results:
                for c in r.competitor_mentions:
                    comp_counts[c] = comp_counts.get(c, 0) + 1

            sorted_comps = sorted(comp_counts.items(), key=lambda x: x[1], reverse=True)[:6]

            if sorted_comps:
                fig = go.Figure(go.Bar(
                    x=[c[1] for c in sorted_comps],
                    y=[c[0] for c in sorted_comps],
                    orientation='h',
                    marker=dict(color='#7C3AED', line=dict(width=0)),
                    text=[str(c[1]) for c in sorted_comps],
                    textposition='outside',
                    textfont=dict(color='#F1F5F9', size=12),
                ))
                fig.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=0, r=40, t=10, b=10),
                    height=250,
                    xaxis=dict(showgrid=False, showticklabels=False),
                    yaxis=dict(showgrid=False, autorange="reversed"),
                    font=dict(family="Inter, sans-serif"),
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No competitor data available.")

    st.markdown('<div class="glass-divider"></div>', unsafe_allow_html=True)

    # ── Detailed Results Table ──
    st.markdown('<div class="section-header">📋 Prompt-by-Prompt Analysis</div>', unsafe_allow_html=True)

    for i, result in enumerate(report.results):
        mentioned_icon = "✅" if result.brand_mentioned else "❌"
        cited_icon = "📎" if result.citation_found else "—"
        sent_emoji = "😊" if result.sentiment == "positive" else "😐" if result.sentiment == "neutral" else "😟"

        with st.expander(f"{mentioned_icon} **{result.ai_engine}** — {result.prompt[:60]}..."):
            col_d1, col_d2, col_d3 = st.columns(3)
            with col_d1:
                st.markdown(f"**Mentioned:** {mentioned_icon} {'Yes' if result.brand_mentioned else 'No'}")
                st.markdown(f"**Position:** {'#' + str(result.position) if result.position > 0 else 'Not ranked'}")
            with col_d2:
                st.markdown(f"**Citation:** {cited_icon} {'Found' if result.citation_found else 'Not cited'}")
                st.markdown(f"**Sentiment:** {sent_emoji} {result.sentiment.title()}")
            with col_d3:
                if result.competitor_mentions:
                    st.markdown(f"**Competitors:** {', '.join(result.competitor_mentions[:3])}")

            if result.response_snippet:
                st.markdown(f"""
                <div style="
                    background: rgba(15, 23, 42, 0.5);
                    border-left: 3px solid #7C3AED;
                    padding: 0.8rem 1rem;
                    border-radius: 0 8px 8px 0;
                    color: #94A3B8;
                    font-size: 0.85rem;
                    margin-top: 0.5rem;
                ">
                    💬 <em>"{result.response_snippet}"</em>
                </div>
                """, unsafe_allow_html=True)
