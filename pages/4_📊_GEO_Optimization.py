"""
Page 4: GEO Optimization — Generative Engine Optimization audit & recommendations.
"""

import streamlit as st
from utils.navigation import render_theme_toggle, render_go_back_button
import plotly.graph_objects as go
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ─── Page Config ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="GEO Optimization | Gyani-Baba",
    page_icon="📊",
    layout="wide",
)
render_theme_toggle()
render_go_back_button()

# Load CSS
css_path = Path(__file__).parent.parent / "assets" / "styles.css"
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

from core.geo_auditor import run_geo_audit
from utils.gemini_client import get_gemini_client

# ─── Header ──────────────────────────────────────────────────────────────────

st.markdown("""
<div class="app-header animate-fade-in">
    <h1>📊 GEO Optimization</h1>
    <p>Audit your content for Generative Engine Optimization — rank better in AI search</p>
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

# ─── Run Audit ───────────────────────────────────────────────────────────────

if "geo_audit_report" not in st.session_state:
    st.session_state.geo_audit_report = None

doc = st.session_state.document_content

# Get fact-check score if available
fact_check_score = -1
if st.session_state.get("fact_check_report"):
    fact_check_score = st.session_state.fact_check_report.overall_trust_score

if st.button("🚀 Run GEO Audit", type="primary", use_container_width=True):
    try:
        client = get_gemini_client()
        with st.spinner("📊 Running comprehensive GEO audit... This may take 20-40 seconds."):
            report = run_geo_audit(
                document_text=doc.full_text,
                client=client,
                fact_check_score=fact_check_score,
            )
            st.session_state.geo_audit_report = report
            st.rerun()
    except Exception as e:
        st.error(f"❌ Audit failed: {e}")

# ─── Display Results ─────────────────────────────────────────────────────────

if st.session_state.geo_audit_report is not None:
    report = st.session_state.geo_audit_report

    # ── Overall Score ──
    score = report.overall_score
    score_color = "#10B981" if score >= 70 else "#F59E0B" if score >= 40 else "#EF4444"

    st.markdown(f"""
    <div class="trust-gauge animate-fade-in" style="margin-bottom: 1.5rem;">
        <div style="font-size: 0.8rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5rem;">
            GEO Readiness Score
        </div>
        <div class="score-value" style="color: {score_color};">
            {score:.0f}/100
        </div>
        <div class="score-label">
            {"Excellent — AI-ready content" if score >= 80 else "Good — minor improvements needed" if score >= 60 else "Needs Work — significant optimization required" if score >= 40 else "Poor — major restructuring needed"}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Radar Chart ──
    if report.categories:
        categories = report.categories
        cat_names = [c.category.split("(")[0].strip() for c in categories]
        cat_scores = [c.score for c in categories]

        # Close the radar
        cat_names_closed = cat_names + [cat_names[0]]
        cat_scores_closed = cat_scores + [cat_scores[0]]

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=cat_scores_closed,
            theta=cat_names_closed,
            fill='toself',
            fillcolor='rgba(124, 58, 237, 0.15)',
            line=dict(color='#7C3AED', width=2),
            marker=dict(size=6, color='#8B5CF6'),
            name='GEO Score',
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    showticklabels=True,
                    tickfont=dict(color='#64748B', size=10),
                    gridcolor='rgba(148, 163, 184, 0.1)',
                ),
                angularaxis=dict(
                    showticklabels=True,
                    tickfont=dict(color='#F1F5F9', size=11),
                    gridcolor='rgba(148, 163, 184, 0.1)',
                ),
                bgcolor='rgba(0,0,0,0)',
            ),
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=60, r=60, t=30, b=30),
            height=400,
            font=dict(family="Inter, sans-serif"),
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="glass-divider"></div>', unsafe_allow_html=True)

    # ── Priority Actions ──
    if report.priority_actions:
        st.markdown('<div class="section-header">🎯 Priority Actions</div>', unsafe_allow_html=True)
        st.markdown(
            '<p class="section-subheader">The most impactful steps to improve your AI search visibility</p>',
            unsafe_allow_html=True,
        )

        for i, action in enumerate(report.priority_actions):
            st.markdown(f"""
            <div class="glass-card" style="
                padding: 0.8rem 1.2rem;
                margin-bottom: 0.5rem;
                border-left: 3px solid #7C3AED;
                display: flex;
                align-items: center;
                gap: 0.8rem;
            ">
                <div style="
                    background: rgba(124, 58, 237, 0.2);
                    color: #8B5CF6;
                    font-weight: 700;
                    width: 28px;
                    height: 28px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 0.8rem;
                    flex-shrink: 0;
                ">{i + 1}</div>
                <div style="color: #F1F5F9; font-size: 0.9rem;">{action}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="glass-divider"></div>', unsafe_allow_html=True)

    # ── Category Breakdown ──
    st.markdown('<div class="section-header">📋 Category Breakdown</div>', unsafe_allow_html=True)

    for cat in report.categories:
        cat_color = "#10B981" if cat.score >= 70 else "#F59E0B" if cat.score >= 40 else "#EF4444"

        with st.expander(f"{cat.icon} **{cat.category}** — {cat.score:.0f}/100", expanded=cat.score < 60):
            # Score bar
            st.markdown(f"""
            <div style="margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
                    <span style="color: #94A3B8; font-size: 0.8rem;">Score</span>
                    <span style="color: {cat_color}; font-weight: 700;">{cat.score:.0f}/100</span>
                </div>
                <div class="score-bar-container" style="height: 10px;">
                    <div class="score-bar-fill" style="width: {cat.score}%; background: {cat_color};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            col_f, col_r = st.columns(2)

            with col_f:
                st.markdown("**🔍 Findings**")
                for finding in cat.findings:
                    st.markdown(f"- {finding}")

            with col_r:
                st.markdown("**💡 Recommendations**")
                for rec in cat.recommendations:
                    st.markdown(f"- {rec}")
