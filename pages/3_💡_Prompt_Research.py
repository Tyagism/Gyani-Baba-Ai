"""
Page 3: Prompt Research — Discover what users ask AI about your topic.
"""

import streamlit as st
from utils.navigation import render_theme_toggle, render_go_back_button
import plotly.graph_objects as go
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ─── Page Config ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Prompt Research | Gyani-Baba",
    page_icon="💡",
    layout="wide",
)
render_theme_toggle()
render_go_back_button()

# Load CSS
css_path = Path(__file__).parent.parent / "assets" / "styles.css"
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

from core.prompt_research import research_prompts
from utils.gemini_client import get_gemini_client

# ─── Header ──────────────────────────────────────────────────────────────────

st.markdown("""
<div class="app-header animate-fade-in">
    <h1>💡 Prompt Research</h1>
    <p>Discover what prompts users ask AI engines about your topic & content</p>
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

# ─── Run Research ────────────────────────────────────────────────────────────

if "prompt_research" not in st.session_state:
    st.session_state.prompt_research = None

doc = st.session_state.document_content

if st.button("🚀 Discover Relevant Prompts", type="primary", use_container_width=True):
    try:
        client = get_gemini_client()
        with st.spinner("💡 Researching prompts and content gaps... This may take 20-40 seconds."):
            result = research_prompts(
                document_text=doc.full_text,
                client=client,
                num_prompts=12,
            )
            st.session_state.prompt_research = result
            st.rerun()
    except Exception as e:
        st.error(f"❌ Research failed: {e}")

# ─── Display Results ─────────────────────────────────────────────────────────

if st.session_state.prompt_research is not None:
    result = st.session_state.prompt_research

    # Seed topic
    st.markdown(f"""
    <div class="glass-card animate-fade-in">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <div style="font-size: 2rem;">🎯</div>
            <div>
                <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em;">
                    Detected Topic
                </div>
                <div style="color: #F1F5F9; font-size: 1.3rem; font-weight: 700;">
                    {result.seed_topic}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Tabs ──
    tab_prompts, tab_gaps = st.tabs(["🔍 Discovered Prompts", "🕳️ Content Gaps"])

    with tab_prompts:
        st.markdown('<div class="section-header">Prompts Users Ask AI Engines</div>', unsafe_allow_html=True)
        st.markdown(
            '<p class="section-subheader">These are natural-language queries users type into ChatGPT, Perplexity, and Google AI. '
            'Relevance score shows how well your document answers each prompt.</p>',
            unsafe_allow_html=True,
        )

        # Intent color map
        intent_colors = {
            "informational": "#3B82F6",
            "transactional": "#10B981",
            "navigational": "#F59E0B",
            "comparison": "#8B5CF6",
        }

        for i, prompt_text in enumerate(result.discovered_prompts):
            intent = result.prompt_intents.get(prompt_text, "informational")
            relevance = result.relevance_scores.get(prompt_text, 0.5)
            rel_pct = int(relevance * 100)
            intent_color = intent_colors.get(intent, "#94A3B8")

            rel_color = "#10B981" if rel_pct >= 70 else "#F59E0B" if rel_pct >= 40 else "#EF4444"

            st.markdown(f"""
            <div class="glass-card" style="padding: 1rem 1.2rem; margin-bottom: 0.5rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
                    <div style="flex: 1; min-width: 200px;">
                        <div style="color: #F1F5F9; font-size: 0.95rem; font-weight: 500; margin-bottom: 0.3rem;">
                            💬 "{prompt_text}"
                        </div>
                        <span style="
                            display: inline-block;
                            padding: 0.15rem 0.5rem;
                            background: {intent_color}22;
                            border: 1px solid {intent_color}44;
                            border-radius: 20px;
                            color: {intent_color};
                            font-size: 0.7rem;
                            font-weight: 600;
                            text-transform: uppercase;
                        ">{intent}</span>
                    </div>
                    <div style="text-align: right; min-width: 120px;">
                        <div style="font-size: 0.7rem; color: #94A3B8;">Relevance</div>
                        <div style="font-size: 1.2rem; font-weight: 700; color: {rel_color};">{rel_pct}%</div>
                        <div class="score-bar-container" style="width: 100px;">
                            <div class="score-bar-fill" style="width: {rel_pct}%; background: {rel_color};"></div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Relevance distribution chart
        if result.relevance_scores:
            st.markdown('<div class="glass-divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="section-header">📊 Relevance Distribution</div>', unsafe_allow_html=True)

            scores = list(result.relevance_scores.values())
            prompts = [p[:40] + "..." if len(p) > 40 else p for p in result.relevance_scores.keys()]

            colors = ['#10B981' if s >= 0.7 else '#F59E0B' if s >= 0.4 else '#EF4444' for s in scores]

            fig = go.Figure(go.Bar(
                x=[s * 100 for s in scores],
                y=prompts,
                orientation='h',
                marker=dict(color=colors, line=dict(width=0)),
                text=[f"{s*100:.0f}%" for s in scores],
                textposition='outside',
                textfont=dict(color='#F1F5F9', size=11),
            ))
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=50, t=10, b=10),
                height=max(len(scores) * 35, 200),
                xaxis=dict(range=[0, 110], showgrid=False, showticklabels=False),
                yaxis=dict(showgrid=False, autorange="reversed"),
                font=dict(family="Inter, sans-serif", size=11),
            )
            st.plotly_chart(fig, use_container_width=True)

    with tab_gaps:
        st.markdown('<div class="section-header">🕳️ Content Gaps</div>', unsafe_allow_html=True)
        st.markdown(
            '<p class="section-subheader">Important questions users ask that your document does NOT answer well. '
            'Filling these gaps will improve your AI search visibility.</p>',
            unsafe_allow_html=True,
        )

        if result.content_gaps:
            for i, gap in enumerate(result.content_gaps):
                st.markdown(f"""
                <div class="glass-card" style="padding: 1rem 1.2rem; margin-bottom: 0.5rem; border-left: 3px solid #EF4444;">
                    <div style="display: flex; align-items: center; gap: 0.8rem;">
                        <div style="font-size: 1.3rem;">⚠️</div>
                        <div style="color: #F1F5F9; font-size: 0.9rem;">{gap}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ No major content gaps detected!")
