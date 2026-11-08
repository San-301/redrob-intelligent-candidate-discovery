# src/ui/components.py
"""
Reusable UI components for the Redrob Intelligent Candidate Discovery web app.
Designed with clean, native Streamlit containers to prevent raw HTML code-block rendering.
"""
from typing import Dict, List, Any
import streamlit as st
import pandas as pd
import plotly.express as px

from src.validation.honeypot_detector import HoneypotDetector
from src.reasoning.skill_matcher import SkillMatcher

def get_tier_badge(score: float, is_honeypot: bool) -> tuple:
    """Returns (tier_label, badge_color_style)"""
    if is_honeypot:
        return "⚠️ Risk Flagged", "background:#FEF2F2; color:#B91C1C; border:1px solid #FECACA;"
    if score >= 0.94:
        return "★ Top Tier Match", "background:#ECFDF5; color:#047857; border:1px solid #A7F3D0;"
    elif score >= 0.85:
        return "Strong Match", "background:#F0F9FF; color:#0369A1; border:1px solid #BAE6FD;"
    elif score >= 0.70:
        return "Good Match", "background:#F8FAFC; color:#334155; border:1px solid #CBD5E1;"
    else:
        return "Adjacent Profile", "background:#F8FAFC; color:#64748B; border:1px solid #E2E8F0;"

def render_header():
    """Renders the executive app header."""
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); color: #F8FAFC; padding: 1.5rem 1.75rem; border-radius: 12px; margin-bottom: 1.25rem; border: 1px solid #334155;">
            <div style="margin-bottom: 0.4rem;">
                <span style="display:inline-block; padding:0.2rem 0.55rem; font-size:0.75rem; font-weight:700; border-radius:9999px; background:#334155; color:#38BDF8; margin-right:0.4rem;">PRODUCTION RECRUITER AI</span>
                <span style="display:inline-block; padding:0.2rem 0.55rem; font-size:0.75rem; font-weight:700; border-radius:9999px; background:#064E3B; color:#6EE7B7; margin-right:0.4rem;">DETERMINISTIC & ZERO HALLUCINATION</span>
                <span style="display:inline-block; padding:0.2rem 0.55rem; font-size:0.75rem; font-weight:700; border-radius:9999px; background:#701A75; color:#F472B6;">HONEYPOT DEFENSE ACTIVE</span>
            </div>
            <h2 style="margin: 0.35rem 0 0.25rem 0; font-size: 1.65rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em;">
                Redrob Intelligent Candidate Discovery
            </h2>
            <p style="margin: 0; font-size: 0.9rem; color: #94A3B8;">
                Production-grade talent discovery and ranking system. Ingests candidate pools, detects profile inflation & synthetic honeypots, and evaluates candidate DNA against technical job descriptions with transparent, explainable reasoning.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_kpis(summary: Dict[str, Any]):
    """Renders high-level KPI cards using native Streamlit columns."""
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        with st.container(border=True):
            st.caption("TOTAL INGESTED")
            st.markdown(f"### {summary.get('total_candidates', 0):,}")
            st.caption("Candidate pool")

    with col2:
        with st.container(border=True):
            st.caption("RANKED MATCHES")
            st.markdown(f"### {summary.get('ranked_count', 0)}")
            st.caption("Top recommendations")

    with col3:
        with st.container(border=True):
            st.caption("HONEYPOTS FLAGGED")
            flagged = summary.get('honeypots_count', 0)
            color = "#DC2626" if flagged > 0 else "#0F172A"
            st.markdown(f"<h3 style='color:{color}; margin:0;'>{flagged}</h3>", unsafe_allow_html=True)
            st.caption("Anomalies penalized")

    with col4:
        with st.container(border=True):
            st.caption("AVG TOP SCORE")
            st.markdown(f"### {summary.get('avg_score', 0.0):.3f}")
            st.caption("Range 0.0 – 1.0")

    with col5:
        with st.container(border=True):
            st.caption("OPEN TO WORK")
            st.markdown(f"### {summary.get('open_to_work_pct', 0.0):.1f}%")
            st.caption("Immediate availability")

def render_candidate_card(candidate: Dict, rank: int, raw_candidate: Dict = None, jd_text: str = ""):
    """
    Renders a compact, uncluttered, professional candidate card using native Streamlit containers.
    Prevents raw HTML block issues and avoids visual overwhelm.
    """
    cf = candidate.get("candidate_features", {})
    feat = candidate.get("features", {})
    score = candidate.get("score", 0.0)
    cid = candidate.get("candidate_id", "N/A")
    title = str(cf.get("current_title", "Candidate")).title()
    company = str(cf.get("current_company", "N/A")).title()
    exp = cf.get("years_experience", 0.0)
    
    # Check honeypot flags
    hd = HoneypotDetector()
    hp_info = hd.inspect(raw_candidate or {}, cf) if raw_candidate else {"is_suspicious": False, "flags": [], "penalty": 0.0}
    is_honeypot = hp_info.get("penalty", 0.0) > 0.15
    
    tier_label, tier_style = get_tier_badge(score, is_honeypot)
    
    # Rank badge color
    if rank == 1:
        rank_badge = "background:#FEF3C7; color:#92400E; border:1px solid #FCD34D;"
    elif rank == 2:
        rank_badge = "background:#F1F5F9; color:#334155; border:1px solid #CBD5E1;"
    elif rank == 3:
        rank_badge = "background:#FFEDD5; color:#9A3412; border:1px solid #FDBA74;"
    else:
        rank_badge = "background:#F8FAFC; color:#64748B; border:1px solid #E2E8F0;"

    with st.container(border=True):
        # Top Row: Rank, Title, Company, Score, Tier
        rcol1, rcol2 = st.columns([3, 1])
        with rcol1:
            st.markdown(
                f"""
                <div style="display:flex; align-items:center; gap:0.6rem; flex-wrap:wrap;">
                    <span style="display:inline-flex; align-items:center; justify-content:center; width:2rem; height:2rem; border-radius:6px; font-weight:800; font-size:0.9rem; {rank_badge}">#{rank}</span>
                    <strong style="font-size:1.1rem; color:#0F172A;">{title}</strong>
                    <span style="color:#64748B; font-size:0.9rem;">at <strong style="color:#1E293B;">{company}</strong></span>
                    <span style="color:#94A3B8; font-size:0.85rem;">&bull; {exp:.1f} yrs exp &bull; <code>{cid}</code></span>
                </div>
                """,
                unsafe_allow_html=True
            )
        with rcol2:
            st.markdown(
                f"""
                <div style="text-align:right;">
                    <span style="display:inline-block; padding:0.25rem 0.65rem; border-radius:9999px; font-weight:800; font-family:monospace; font-size:0.95rem; {tier_style}">{score:.4f}</span>
                    <div style="font-size:0.75rem; color:#64748B; font-weight:600; margin-top:0.15rem;">{tier_label}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # AI Reasoning Callout (clean, uncluttered box)
        st.markdown(
            f"""
            <div style="background:#F8FAFC; border-left:3px solid #0284C7; border-radius:4px; padding:0.5rem 0.75rem; margin:0.4rem 0; font-size:0.85rem; color:#1E293B; line-height:1.45;">
                <strong>AI Evaluation:</strong> {candidate.get('reasoning', '')}
            </div>
            """,
            unsafe_allow_html=True
        )

        # Matched Skills & Signals Row (compact pills)
        chips = []
        if jd_text and raw_candidate:
            matcher = SkillMatcher()
            match_res = matcher.match(raw_candidate, jd_text)
            for s in match_res.get("matched_skills", [])[:4]:
                chips.append(f'<span style="background:#F0FDF4; color:#166534; border:1px solid #BBF7D0; padding:0.15rem 0.45rem; border-radius:4px; font-size:0.75rem; font-weight:600;">✓ {s}</span>')

        if cf.get("open_to_work"):
            chips.append('<span style="background:#ECFDF5; color:#065F46; border:1px solid #A7F3D0; padding:0.15rem 0.45rem; border-radius:4px; font-size:0.75rem; font-weight:600;">● Open to Work</span>')
        
        np_days = cf.get("notice_period", 90)
        chips.append(f'<span style="background:#F8FAFC; color:#475569; border:1px solid #E2E8F0; padding:0.15rem 0.45rem; border-radius:4px; font-size:0.75rem;">⏱ {np_days}d Notice</span>')

        gh = cf.get("github_score", 0)
        if gh > 0:
            chips.append(f'<span style="background:#F8FAFC; color:#475569; border:1px solid #E2E8F0; padding:0.15rem 0.45rem; border-radius:4px; font-size:0.75rem;">💻 GitHub {gh:.0f}</span>')

        if is_honeypot:
            chips.append(f'<span style="background:#FEF2F2; color:#991B1B; border:1px solid #FECACA; padding:0.15rem 0.45rem; border-radius:4px; font-size:0.75rem; font-weight:700;">⚠️ Honeypot (-{hp_info["penalty"]:.2f})</span>')

        st.markdown(f"<div style='display:flex; flex-wrap:wrap; gap:0.35rem; align-items:center;'>{' '.join(chips)}</div>", unsafe_allow_html=True)

        # Expandable Details (keeps card uncluttered by default!)
        with st.expander(f"🔍 View Profile Details & Career History ({cid})", expanded=False):
            prof = (raw_candidate or {}).get("profile", {})
            career = (raw_candidate or {}).get("career_history", [])
            skills = (raw_candidate or {}).get("skills", [])
            
            dcol1, dcol2 = st.columns([1, 1])
            with dcol1:
                st.markdown("**Headline / Summary:**")
                st.caption(prof.get("headline") or prof.get("summary") or "No headline provided.")
                if is_honeypot:
                    st.error("🚨 **Triggered Risk Flags:**")
                    for flag in hp_info.get("flags", []):
                        st.markdown(f"- {flag}")
            with dcol2:
                st.markdown("**Key Platform Metrics:**")
                st.markdown(f"- **Response Rate:** {cf.get('response_rate', 0)*100:.0f}%")
                st.markdown(f"- **Interview Rate:** {cf.get('interview_completion', 0)*100:.0f}%")
                st.markdown(f"- **AI Skill Count:** {cf.get('ai_skill_count', 0)}")
                st.markdown(f"- **Retrieval Skills:** {cf.get('retrieval_skill_count', 0)}")
            
            if career:
                st.markdown("**Career History:**")
                for job in career:
                    dur = job.get('duration_months', 0)
                    st.markdown(f"- **{job.get('title')}** at **{job.get('company')}** ({dur} mos): _{job.get('description', '')}_")


def render_candidate_deep_dive(candidate: Dict, raw_candidate: Dict, jd_text: str = ""):
    """Renders comprehensive full-profile analysis drawer/tab."""
    cf = candidate.get("candidate_features", {})
    feat = candidate.get("features", {})
    score = candidate.get("score", 0.0)
    cid = candidate.get("candidate_id", "N/A")
    prof = raw_candidate.get("profile", {})
    career = raw_candidate.get("career_history", [])
    skills = raw_candidate.get("skills", [])
    signals = raw_candidate.get("redrob_signals", {})
    
    with st.container(border=True):
        st.markdown(f"### 👤 Profile Dossier: **{prof.get('current_title', 'Candidate')}** (`{cid}`)")
        st.markdown(f"**Company:** {prof.get('current_company', 'N/A')} &bull; **Industry:** {prof.get('current_industry', 'N/A')} &bull; **Experience:** {prof.get('years_of_experience', 0)} years")
        
        if prof.get("headline"):
            st.info(f"**Headline:** {prof.get('headline')}")
        if prof.get("summary"):
            st.markdown(f"_{prof.get('summary')}_")
            
        st.markdown("---")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### 🎯 Score Contribution Breakdown")
            score_df = pd.DataFrame([
                {"Component": "Core Experience Match", "Value": feat.get("experience_score", 0) * 0.12},
                {"Component": "Title Relevance", "Value": feat.get("title_score", 0) * 0.12},
                {"Component": "Retrieval & Search Expertise", "Value": feat.get("retrieval_score", 0) * 0.15},
                {"Component": "Applied AI Experience", "Value": feat.get("career_ai_score", 0) * 0.18},
                {"Component": "Production ML Deployments", "Value": feat.get("production_score", 0) * 0.08},
                {"Component": "Evaluation Frameworks (NDCG/MRR)", "Value": feat.get("evaluation_score", 0) * 0.08},
                {"Component": "Company Credibility (Product/AI)", "Value": (feat.get("product_company_score", 0) + feat.get("ai_company_score", 0)) * 0.05},
                {"Component": "Engagement & Platform Signals", "Value": feat.get("engagement_score", 0) * 0.06},
                {"Component": "GitHub Verification", "Value": feat.get("github_score", 0) * 0.04},
                {"Component": "Penalties (Notice/Consulting/Honeypot)", "Value": -(feat.get("notice_penalty", 0)*0.08 + feat.get("consulting_penalty", 0)*0.15 + feat.get("honeypot_penalty", 0)*0.15)}
            ])
            
            fig = px.bar(
                score_df,
                x="Value",
                y="Component",
                orientation="h",
                color="Value",
                color_continuous_scale=[(0, "#EF4444"), (0.5, "#3B82F6"), (1, "#10B981")],
                title=f"Composite Score: {score:.4f}"
            )
            fig.update_layout(height=340, margin=dict(l=0, r=0, t=30, b=0), showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.markdown("#### 🛡️ Honeypot & Consistency Audit")
            hd = HoneypotDetector()
            audit = hd.inspect(raw_candidate, cf)
            if audit["penalty"] > 0:
                st.error(f"⚠️ **Inconsistency Flags Detected! Total Penalty: -{audit['penalty']:.2f}**")
                for flag in audit["flags"]:
                    st.markdown(f"- 🚨 **{flag}**")
            else:
                st.success("✅ **Profile Consistency Clean**: Passed all 11 anti-fraud heuristics.")
                
            st.markdown("#### ⚡ Platform Engagement Signals")
            scol1, scol2 = st.columns(2)
            with scol1:
                st.metric("Notice Period", f"{signals.get('notice_period_days', 90)} days")
                st.metric("Recruiter Response", f"{signals.get('recruiter_response_rate', 0)*100:.0f}%")
                st.metric("Open to Work", "Yes" if signals.get('open_to_work_flag') else "No")
            with scol2:
                st.metric("GitHub Score", f"{signals.get('github_activity_score', 0):.1f}/100")
                st.metric("Interview Rate", f"{signals.get('interview_completion_rate', 0)*100:.0f}%")
                st.metric("Profile Completeness", f"{signals.get('profile_completeness_score', 0):.0f}%")
                
        st.markdown("---")
        
        # Career History Timeline
        st.markdown("#### 💼 Career History")
        if career:
            for job in career:
                duration = job.get('duration_months', 0)
                years_dur = f"{duration // 12}y {duration % 12}m" if duration >= 12 else f"{duration}m"
                st.markdown(f"**{job.get('title', 'Role')}** at **{job.get('company', 'Company')}** (`{years_dur}`)")
                st.caption(job.get('description', ''))
        else:
            st.caption("No career history records reported.")
            
        # Skills List
        st.markdown("#### 🛠️ Claimed Skills Inventory")
        if skills:
            skill_badges = []
            for s in skills:
                p = s.get("proficiency", "intermediate").lower()
                color = "#047857" if p in ["expert", "advanced"] else "#334155"
                bg = "#ECFDF5" if p in ["expert", "advanced"] else "#F1F5F9"
                skill_badges.append(f'<span style="background:{bg}; color:{color}; border:1px solid #CBD5E1; padding:0.2rem 0.5rem; border-radius:6px; font-size:0.8rem; margin:0.2rem; display:inline-block;">{s.get("name")} ({p})</span>')
            st.markdown(" ".join(skill_badges), unsafe_allow_html=True)
            
        with st.expander("🔍 View Raw Candidate JSON Data"):
            st.json(raw_candidate)


def render_comparison_view(candidates: List[Dict], raw_candidates_map: Dict[str, Dict]):
    """Renders head-to-head candidate comparison using native containers."""
    if not candidates:
        st.info("Select 2 or 3 candidates from the Discovery tab to compare them side-by-side.")
        return

    cols = st.columns(len(candidates))
    hd = HoneypotDetector()
    
    for i, candidate in enumerate(candidates):
        cid = candidate["candidate_id"]
        raw = raw_candidates_map.get(cid, {})
        cf = candidate.get("candidate_features", {})
        prof = raw.get("profile", {})
        hp = hd.inspect(raw, cf)
        
        with cols[i]:
            with st.container(border=True):
                st.caption(f"CANDIDATE {i+1} &bull; #{candidate.get('rank', i+1)}")
                st.markdown(f"**{prof.get('current_title', 'Role')}**")
                st.markdown(f"_{prof.get('current_company', 'Company')} ({cid})_")
                
                st.metric("Match Score", f"{candidate['score']:.4f}")
                
                st.markdown("---")
                st.markdown(f"- **Experience:** {prof.get('years_of_experience', 0)} years")
                st.markdown(f"- **Notice Period:** {cf.get('notice_period', 90)} days")
                st.markdown(f"- **Open to Work:** {'Yes' if cf.get('open_to_work') else 'No'}")
                st.markdown(f"- **Retrieval Skills:** {cf.get('retrieval_skill_count', 0)}")
                st.markdown(f"- **AI Skill Count:** {cf.get('ai_skill_count', 0)}")
                st.markdown(f"- **Evaluation Exp:** {'Yes' if cf.get('evaluation_experience') else 'No'}")
                st.markdown(f"- **GitHub Score:** {cf.get('github_score', 0):.0f}/100")
                st.markdown(f"- **Response Rate:** {cf.get('response_rate', 0)*100:.0f}%")
                
                hp_val = hp['penalty']
                if hp_val > 0:
                    st.markdown(f"- **Honeypot Penalty:** :red[-{hp_val:.2f}]")
                else:
                    st.markdown("- **Honeypot Risk:** :green[Clean (0.0)]")
                
                st.info(f"**Reasoning:** {candidate.get('reasoning', '')}")
