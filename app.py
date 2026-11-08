# app.py
"""
Redrob Intelligent Candidate Discovery & Ranking Platform.
Interactive Streamlit Web Application for End-to-End Recruiter Intelligence.
"""
import time
import json
import io
import streamlit as st
import pandas as pd
import plotly.express as px

from src.ui.styles import CUSTOM_CSS
from src.ui.components import (
    render_header,
    render_kpis,
    render_candidate_card,
    render_candidate_deep_dive,
    render_comparison_view
)
from src.ranking.ranker import CandidateRanker
from src.preprocessing.candidate_parser import CandidateParser
from src.preprocessing.jd_parser import JDParser
from src.validation.honeypot_detector import HoneypotDetector
from src.sample_data import get_sample_candidates

# 1. Page Configuration
st.set_page_config(
    page_title="Redrob Intelligent Candidate Discovery",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inject Executive SaaS CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# 3. Session State Initialization
if "candidates" not in st.session_state:
    st.session_state.candidates = []
if "ranked_results" not in st.session_state:
    st.session_state.ranked_results = []
if "selected_candidate_id" not in st.session_state:
    st.session_state.selected_candidate_id = None
if "compare_candidates" not in st.session_state:
    st.session_state.compare_candidates = []
if "execution_stats" not in st.session_state:
    st.session_state.execution_stats = {}
if "data_source_name" not in st.session_state:
    st.session_state.data_source_name = "None"

# JD Presets
JD_PRESETS = {
    "Redrob Challenge: Senior Retrieval & Ranking Engineer": {
        "text": """
We are seeking a Senior AI/ML Engineer specializing in Information Retrieval, Search Relevance, and Recommendation Systems.
Responsibilities:
- Build and optimize two-stage retrieval pipelines combining dense semantic embeddings (Sentence Transformers, FAISS, Qdrant) and sparse lexical search (BM25).
- Develop neural ranking models, learning-to-rank, and cross-encoders for personalized search results.
- Design offline and online evaluation frameworks utilizing NDCG@10, MRR, MAP, and production A/B testing.
- Deploy scalable, low-latency ML microservices in production serving real-time user queries.
Requirements:
- 5 to 9 years of production machine learning experience.
- Strong evidence of shipping real-world retrieval or ranking systems at scale.
- Background in product tech companies or AI-first startups preferred.
- Exclude profiles with unverified skill claims, pure academic research without deployment, or consulting-only backgrounds.
        """.strip(),
        "min_exp": 3,
        "max_exp": 10,
        "skills": ["retrieval", "semantic search", "embeddings", "ranking", "recommendation systems", "llms"]
    },
    "Generative AI & LLM Systems Engineer": {
        "text": """
Looking for a Senior Generative AI Engineer to build scalable RAG architectures and fine-tune foundation models.
Responsibilities:
- Build enterprise vector retrieval augmented generation (RAG) platforms using Qdrant/FAISS, LangChain, and embedding pipelines.
- Fine-tune open-source LLMs using LoRA, QLoRA, and PEFT.
- Evaluate model safety, hallucination rates, and latency.
Requirements:
- 4 to 8 years experience in NLP and deep learning.
        """.strip(),
        "min_exp": 4,
        "max_exp": 8,
        "skills": ["llms", "rag", "embeddings", "vector search", "fine-tuning llms", "pytorch"]
    },
    "Search & Relevance Platform Architect": {
        "text": """
Seeking a Search Architect to lead our search infrastructure, query understanding, and catalog ranking.
Requirements:
- 6 to 12 years building distributed search platforms (Elasticsearch, OpenSearch, Vespa, FAISS).
- Offline evaluation metrics: NDCG, MRR, MAP.
- Proven leadership and high-scale production systems.
        """.strip(),
        "min_exp": 6,
        "max_exp": 12,
        "skills": ["retrieval", "elasticsearch", "opensearch", "ranking", "ndcg", "mrr"]
    }
}

# 4. Sidebar Controls
with st.sidebar:
    st.markdown("### 📥 1. Candidate Data Ingestion")
    
    upload_tab, path_tab, sample_tab = st.tabs(["📁 Upload File", "💻 Local Path", "⚡ Sample"])
    
    with upload_tab:
        uploaded_file = st.file_uploader(
            "Upload Candidate File (.jsonl or .json)",
            type=["jsonl", "json"],
            help="Supports files up to 1GB including the official 465MB hackathon dataset."
        )
        if uploaded_file is not None:
            if st.session_state.get("uploaded_filename") != uploaded_file.name:
                with st.spinner(f"Reading and parsing {uploaded_file.name}..."):
                    try:
                        loaded = []
                        if uploaded_file.name.endswith(".jsonl"):
                            text_stream = io.TextIOWrapper(uploaded_file, encoding="utf-8")
                            for line in text_stream:
                                line = line.strip()
                                if line:
                                    loaded.append(json.loads(line))
                        else:
                            text_stream = io.TextIOWrapper(uploaded_file, encoding="utf-8")
                            loaded_json = json.load(text_stream)
                            loaded = loaded_json if isinstance(loaded_json, list) else [loaded_json]
                            
                        st.session_state.candidates = loaded
                        st.session_state.data_source_name = f"{uploaded_file.name} ({len(loaded):,} profiles)"
                        st.session_state.uploaded_filename = uploaded_file.name
                        st.session_state.ranked_results = []
                        st.success(f"Loaded {len(loaded):,} candidates!")
                    except Exception as e:
                        st.error(f"Error reading file: {e}")

    with path_tab:
        st.caption("For 400MB+ datasets, loading directly from disk avoids browser upload latency:")
        local_path_input = st.text_input("Enter local file path:", value="data/raw/candidates.jsonl")
        if st.button("📂 Load from Local Disk", use_container_width=True):
            from pathlib import Path
            p = Path(local_path_input)
            if not p.exists():
                st.error(f"File not found at: {local_path_input}")
            else:
                with st.spinner(f"Streaming {p.name} from disk..."):
                    try:
                        loaded = []
                        with open(p, "r", encoding="utf-8") as f:
                            for line in f:
                                line = line.strip()
                                if line:
                                    loaded.append(json.loads(line))
                        st.session_state.candidates = loaded
                        st.session_state.data_source_name = f"{p.name} ({len(loaded):,} profiles)"
                        st.session_state.uploaded_filename = None
                        st.session_state.ranked_results = []
                        st.success(f"Loaded {len(loaded):,} candidates from disk!")
                    except Exception as e:
                        st.error(f"Error reading local file: {e}")
                
    with sample_tab:
        st.caption("No dataset file on hand? Load our pre-configured benchmark pool (50 profiles including Tier-1 matches, consulting profiles, and honeypots).")
        if st.button("⚡ Load Benchmark Sample Dataset (50 Profiles)", use_container_width=True):
            st.session_state.candidates = get_sample_candidates()
            st.session_state.data_source_name = "Benchmark Sample Dataset (50 Profiles)"
            st.session_state.uploaded_filename = None
            st.session_state.ranked_results = []
            st.success("Loaded 50 benchmark profiles!")

    # Current Dataset Status
    curr_count = len(st.session_state.candidates)
    if curr_count > 0:
        st.info(f"**Active Pool:** {curr_count:,} candidates\n\n**Source:** `{st.session_state.data_source_name}`")
    else:
        st.warning("⚠️ No candidates loaded yet. Upload a file or load the benchmark sample.")

    st.markdown("---")
    st.markdown("### 📋 2. Job Description & Criteria")
    
    preset_choice = st.selectbox(
        "Select Job Description Preset",
        list(JD_PRESETS.keys()) + ["Custom Job Description"]
    )
    
    if preset_choice != "Custom Job Description":
        preset_data = JD_PRESETS[preset_choice]
        jd_text = st.text_area(
            "Job Description Text",
            value=preset_data["text"],
            height=160
        )
        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            min_exp = st.number_input("Min Experience (Yrs)", value=preset_data["min_exp"], min_value=0, max_value=20)
        with col_exp2:
            max_exp = st.number_input("Max Experience (Yrs)", value=preset_data["max_exp"], min_value=1, max_value=25)
        must_have = preset_data["skills"]
    else:
        jd_text = st.text_area(
            "Paste Custom Job Description",
            value="Seeking a Machine Learning Engineer with experience in search, ranking, embeddings, and python.",
            height=160
        )
        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            min_exp = st.number_input("Min Experience (Yrs)", value=3, min_value=0, max_value=20)
        with col_exp2:
            max_exp = st.number_input("Max Experience (Yrs)", value=10, min_value=1, max_value=25)
        must_have = ["retrieval", "semantic search", "embeddings", "ranking", "python"]

    st.markdown("---")
    st.markdown("### ⚙️ 3. Execution Parameters")
    
    top_k_select = st.slider("Max Candidates to Rank (Top-K)", min_value=10, max_value=100, value=min(100, max(10, curr_count or 100)), step=5)
    exclude_honeypots_toggle = st.checkbox("Strict Honeypot Quarantine (Exclude flagged from Top-K)", value=False)
    
    run_btn = st.button("🚀 Run Candidate Discovery & Ranking", type="primary", use_container_width=True, disabled=(curr_count == 0))

# 5. Core Execution Logic
if run_btn and st.session_state.candidates:
    with st.spinner("Processing candidate DNA, detecting honeypots, and computing composite rankings..."):
        start_time = time.time()
        
        jd_features = {
            "min_exp": min_exp,
            "max_exp": max_exp,
            "must_have_skills": must_have
        }
        
        ranker = CandidateRanker(jd_features)
        
        # Execute ranking with quarantine support (guarantees exactly top_k clean candidates when enabled)
        ranked = ranker.get_top_k(st.session_state.candidates, k=top_k_select, exclude_honeypots=exclude_honeypots_toggle)
        quarantined = getattr(ranker, "last_quarantined", [])
        
        # Honeypot inspection
        hd = HoneypotDetector()
        target_ids = {c["candidate_id"] for c in ranked} | {c["candidate_id"] for c in quarantined}
        raw_map = {c["candidate_id"]: c for c in st.session_state.candidates if c.get("candidate_id") in target_ids}
        
        for cand in ranked:
            raw = raw_map.get(cand["candidate_id"], {})
            cf = cand.get("candidate_features", {})
            cand["honeypot_info"] = hd.inspect(raw, cf)
            
        for cand in quarantined:
            raw = raw_map.get(cand["candidate_id"], {})
            cf = cand.get("candidate_features", {})
            cand["honeypot_info"] = hd.inspect(raw, cf)

        total_honeypots = len(quarantined) if exclude_honeypots_toggle else sum(1 for c in ranked if c.get("honeypot_info", {}).get("penalty", 0) > 0.15)
        elapsed = time.time() - start_time
        
        st.session_state.ranked_results = ranked
        st.session_state.quarantined_candidates = quarantined
        st.session_state.execution_stats = {
            "runtime_seconds": elapsed,
            "total_evaluated": len(st.session_state.candidates),
            "ranked_count": len(ranked),
            "honeypots_detected": total_honeypots,
            "jd_text": jd_text,
            "jd_features": jd_features
        }
        st.toast(f"Candidate ranking complete in {elapsed:.2f} seconds!", icon="✅")

# 6. Main Dashboard Area
render_header()

# If ranking has been performed, display KPIs
if st.session_state.ranked_results:
    ranked_pool = st.session_state.ranked_results
    scores = [c["score"] for c in ranked_pool]
    otw_count = sum(1 for c in ranked_pool if c.get("candidate_features", {}).get("open_to_work"))
    
    kpi_data = {
        "total_candidates": st.session_state.execution_stats.get("total_evaluated", len(st.session_state.candidates)),
        "ranked_count": len(ranked_pool),
        "honeypots_count": st.session_state.execution_stats.get("honeypots_detected", 0),
        "avg_score": (sum(scores) / len(scores)) if scores else 0.0,
        "open_to_work_pct": (otw_count / len(ranked_pool) * 100) if ranked_pool else 0.0
    }
    render_kpis(kpi_data)
else:
    # Initial landing callout
    st.markdown(
        """
        <div class="callout-box info">
            <strong>Welcome to the Redrob Intelligent Candidate Discovery Platform.</strong><br>
            To begin, upload your <code>candidates.jsonl</code> file in the left sidebar, or click 
            <strong>'⚡ Load Benchmark Sample Dataset'</strong> to evaluate candidate discovery immediately.
        </div>
        """,
        unsafe_allow_html=True
    )

# 7. Navigation Tabs
tab_discovery, tab_profile, tab_compare, tab_honeypot, tab_analytics = st.tabs([
    "🎯 Candidate Discovery & Ranking",
    "👤 Candidate Deep Dive",
    "⚖️ Candidate Comparison Lab",
    "🛡️ Honeypot & Risk Lab",
    "📊 Talent Pool Analytics"
])

# Create fast lookup map for ranked and quarantined candidates
audit_ids = {c["candidate_id"] for c in st.session_state.ranked_results} | {c["candidate_id"] for c in st.session_state.get("quarantined_candidates", [])}
raw_candidates_map = {c["candidate_id"]: c for c in st.session_state.candidates if c["candidate_id"] in audit_ids}

# =========================================================================
# TAB 1: CANDIDATE DISCOVERY & RANKING
# =========================================================================
with tab_discovery:
    if not st.session_state.ranked_results:
        st.info("👈 Load candidates and click 'Run Candidate Discovery & Ranking' in the sidebar to view ranked candidates.")
    else:
        ranked_list = st.session_state.ranked_results
        
        # Filter & Search Toolbar
        st.markdown("#### 🔍 Filter & Search Talent Pool")
        fcol1, fcol2, fcol3, fcol4 = st.columns([2, 1, 1, 1])
        
        with fcol1:
            search_query = st.text_input("Search by Title, Company, or Candidate ID", placeholder="e.g. Machine Learning, Observe.AI, CAND_0001001...")
            
        with fcol2:
            min_score_filter = st.slider("Min Match Score", min_value=0.0, max_value=1.0, value=0.0, step=0.05)
            
        with fcol3:
            notice_filter = st.selectbox("Max Notice Period", ["All", "<= 30 Days", "<= 60 Days", "<= 90 Days"])
            
        with fcol4:
            otw_only = st.checkbox("Open to Work Only", value=False)
            clean_only = st.checkbox("Exclude Risk Flagged", value=False)

        # Apply Filters
        filtered_candidates = []
        for c in ranked_list:
            cf = c.get("candidate_features", {})
            raw = raw_candidates_map.get(c["candidate_id"], {})
            prof = raw.get("profile", {})
            score = c.get("score", 0.0)
            
            # Score filter
            if score < min_score_filter:
                continue
                
            # Search query
            if search_query:
                q = search_query.lower()
                text_blob = f"{c['candidate_id']} {prof.get('current_title', '')} {prof.get('current_company', '')} {c.get('reasoning', '')}".lower()
                if q not in text_blob:
                    continue
                    
            # Notice filter
            np_days = cf.get("notice_period", 90)
            if notice_filter == "<= 30 Days" and np_days > 30:
                continue
            elif notice_filter == "<= 60 Days" and np_days > 60:
                continue
            elif notice_filter == "<= 90 Days" and np_days > 90:
                continue
                
            # OTW filter
            if otw_only and not cf.get("open_to_work"):
                continue
                
            # Clean only
            if clean_only and c.get("honeypot_info", {}).get("penalty", 0) > 0.15:
                continue
                
            filtered_candidates.append(c)

        st.caption(f"Showing **{len(filtered_candidates)}** of **{len(ranked_list)}** ranked candidates.")
        
        # View Options & Exports
        vcol1, vcol2 = st.columns([1, 1])
        with vcol1:
            view_mode = st.radio("Display View", ["Card View (Detailed)", "Interactive Table View"], horizontal=True)
            
        with vcol2:
            st.markdown("<div style='text-align: right;'>", unsafe_allow_html=True)
            # Official Submission CSV generator
            sub_rows = [
                {
                    "candidate_id": c["candidate_id"],
                    "rank": idx,
                    "score": c["score"],
                    "reasoning": c["reasoning"]
                }
                for idx, c in enumerate(filtered_candidates, start=1)
            ]
            sub_df = pd.DataFrame(sub_rows)
            sub_csv = sub_df.to_csv(index=False).encode('utf-8')
            
            # Comprehensive export with all features
            full_rows = []
            for idx, c in enumerate(filtered_candidates, start=1):
                raw = raw_candidates_map.get(c["candidate_id"], {})
                cf = c.get("candidate_features", {})
                full_rows.append({
                    "rank": idx,
                    "candidate_id": c["candidate_id"],
                    "match_score": c["score"],
                    "title": raw.get("profile", {}).get("current_title", ""),
                    "company": raw.get("profile", {}).get("current_company", ""),
                    "years_experience": raw.get("profile", {}).get("years_of_experience", 0),
                    "notice_period_days": cf.get("notice_period", 90),
                    "open_to_work": cf.get("open_to_work", 0),
                    "github_score": cf.get("github_score", 0),
                    "retrieval_skills": cf.get("retrieval_skill_count", 0),
                    "ai_skills": cf.get("ai_skill_count", 0),
                    "honeypot_penalty": c.get("honeypot_info", {}).get("penalty", 0),
                    "reasoning": c["reasoning"]
                })
            full_df = pd.DataFrame(full_rows)
            full_csv = full_df.to_csv(index=False).encode('utf-8')
            
            dcol1, dcol2 = st.columns(2)
            with dcol1:
                st.download_button(
                    "📥 Download Official Submission CSV",
                    data=sub_csv,
                    file_name="submission.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            with dcol2:
                st.download_button(
                    "📊 Download Comprehensive Report CSV",
                    data=full_csv,
                    file_name="candidate_discovery_report.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")

        # Render View
        active_jd_text = st.session_state.execution_stats.get("jd_text", "")
        
        if view_mode == "Card View (Detailed)":
            pcol1, pcol2 = st.columns([3, 1])
            with pcol2:
                page_size_option = st.selectbox("Per Page", [10, 20, 50, "All"], index=0)
            
            total_items = len(filtered_candidates)
            if page_size_option == "All":
                page_size = total_items
                total_pages = 1
                curr_page = 1
            else:
                page_size = int(page_size_option)
                total_pages = max(1, (total_items + page_size - 1) // page_size)
                with pcol1:
                    curr_page = st.selectbox("Page", range(1, total_pages + 1), index=0) if total_pages > 1 else 1

            start_idx = (curr_page - 1) * page_size
            end_idx = min(start_idx + page_size, total_items)
            page_candidates = filtered_candidates[start_idx:end_idx]

            for c in page_candidates:
                raw = raw_candidates_map.get(c["candidate_id"], {})
                render_candidate_card(c, c["rank"], raw_candidate=raw, jd_text=active_jd_text)
        else:
            # Table View
            table_rows = []
            for c in filtered_candidates:
                raw = raw_candidates_map.get(c["candidate_id"], {})
                cf = c.get("candidate_features", {})
                hp = c.get("honeypot_info", {})
                table_rows.append({
                    "Rank": c["rank"],
                    "Score": round(c["score"], 4),
                    "Candidate ID": c["candidate_id"],
                    "Title": raw.get("profile", {}).get("current_title", "N/A"),
                    "Company": raw.get("profile", {}).get("current_company", "N/A"),
                    "Exp (Yrs)": raw.get("profile", {}).get("years_of_experience", 0),
                    "Notice": f"{cf.get('notice_period', 90)}d",
                    "Open to Work": "✓ Yes" if cf.get("open_to_work") else "No",
                    "GitHub": f"{cf.get('github_score', 0):.0f}",
                    "Risk Flagged": "⚠️ Yes" if hp.get("penalty", 0) > 0.15 else "Clean",
                    "Evaluation Reasoning": c["reasoning"]
                })
            st.dataframe(pd.DataFrame(table_rows), use_container_width=True, height=600)

# =========================================================================
# TAB 2: CANDIDATE DEEP DIVE
# =========================================================================
with tab_profile:
    if not st.session_state.ranked_results:
        st.info("Run candidate ranking to inspect individual candidate dossiers.")
    else:
        cand_options = [
            f"#{c['rank']} - {c['candidate_id']} ({raw_candidates_map.get(c['candidate_id'], {}).get('profile', {}).get('current_title', 'Role')} at {raw_candidates_map.get(c['candidate_id'], {}).get('profile', {}).get('current_company', 'Company')}) - Score: {c['score']:.4f}"
            for c in st.session_state.ranked_results
        ]
        
        selected_idx_str = st.selectbox("Select Candidate to Inspect:", cand_options)
        selected_cid = selected_idx_str.split(" - ")[1].split(" ")[0]
        
        target_cand = next((c for c in st.session_state.ranked_results if c["candidate_id"] == selected_cid), None)
        target_raw = raw_candidates_map.get(selected_cid, {})
        
        if target_cand and target_raw:
            render_candidate_deep_dive(target_cand, target_raw, jd_text=st.session_state.execution_stats.get("jd_text", ""))

# =========================================================================
# TAB 3: CANDIDATE COMPARISON LAB
# =========================================================================
with tab_compare:
    if not st.session_state.ranked_results:
        st.info("Run ranking to compare candidates head-to-head.")
    else:
        st.markdown("#### ⚖️ Head-to-Head Candidate Comparison")
        st.caption("Select 2 or 3 candidates from the ranked pool to compare their experience, skill DNA, and risk profiles.")
        
        compare_options = [
            f"{c['candidate_id']} | #{c['rank']} {raw_candidates_map.get(c['candidate_id'], {}).get('profile', {}).get('current_title', 'Role')} ({raw_candidates_map.get(c['candidate_id'], {}).get('profile', {}).get('current_company', 'Company')})"
            for c in st.session_state.ranked_results
        ]
        
        default_compare = compare_options[:2] if len(compare_options) >= 2 else compare_options
        selected_compare_items = st.multiselect("Choose Candidates to Compare (Max 3):", compare_options, default=default_compare, max_selections=3)
        
        if selected_compare_items:
            selected_cids = [item.split(" | ")[0] for item in selected_compare_items]
            candidates_to_compare = [c for c in st.session_state.ranked_results if c["candidate_id"] in selected_cids]
            render_comparison_view(candidates_to_compare, raw_candidates_map)
        else:
            st.info("Select at least 2 candidates above to view comparison.")

# =========================================================================
# TAB 4: HONEYPOT & RISK LAB
# =========================================================================
with tab_honeypot:
    st.markdown("#### 🛡️ Honeypot & Profile Inconsistency Detection Lab")
    st.markdown(
        """
        The Redrob challenge dataset contains intentionally misleading or synthetic profiles (**honeypots**).
        Our rule engine tests 11 defensive checks to prevent inflated or synthetic profiles from gaming the ranking.
        """
    )
    
    if not st.session_state.ranked_results:
        st.info("Run candidate ranking to audit the dataset for honeypots.")
    else:
        hd = HoneypotDetector()
        audit_records = []
        rule_violations_count = {}
        
        # Collect all candidates flagged across the dataset (both quarantined and ranked)
        flagged_candidates = []
        seen_ids = set()
        
        for cand in st.session_state.get("quarantined_candidates", []):
            cid = cand["candidate_id"]
            if cid not in seen_ids:
                seen_ids.add(cid)
                flagged_candidates.append(cand)
                
        for cand in st.session_state.ranked_results:
            cid = cand["candidate_id"]
            if cid not in seen_ids and cand.get("honeypot_info", {}).get("penalty", 0) > 0:
                seen_ids.add(cid)
                flagged_candidates.append(cand)
        
        for cand in flagged_candidates:
            cid = cand["candidate_id"]
            raw = raw_candidates_map.get(cid, {})
            cf = cand.get("candidate_features", {})
            prof = raw.get("profile", {})
            
            cf = cand.get("candidate_features", {})
            penalty = cf.get("honeypot_penalty", 0.0)
            flags = cf.get("honeypot_flags", [])
            
            if penalty == 0 and cand.get("honeypot_info"):
                penalty = cand["honeypot_info"].get("penalty", 0.0)
                flags = cand["honeypot_info"].get("flags", [])
            elif penalty == 0 and raw:
                ins = hd.inspect(raw, cf)
                penalty = ins.get("penalty", 0.0)
                flags = ins.get("flags", [])

            if penalty > 0:
                for f in flags:
                    rule_violations_count[f] = rule_violations_count.get(f, 0) + 1
                is_quarantined = any(q["candidate_id"] == cid for q in st.session_state.get("quarantined_candidates", []))
                audit_records.append({
                    "Candidate ID": cid,
                    "Status": "🛡️ Quarantined" if is_quarantined else f"Rank #{cand.get('rank', 'N/A')}",
                    "Score": round(cand.get("score", 0), 4),
                    "Title": str(prof.get("current_title") or cf.get("current_title", "Candidate")).title(),
                    "Company": str(prof.get("current_company") or cf.get("current_company", "N/A")).title(),
                    "Experience": f"{prof.get('years_of_experience', cf.get('years_experience', 0))} yrs",
                    "Honeypot Penalty": f"-{penalty:.2f}",
                    "Triggered Violations": " | ".join(flags)
                })
                
        hcol1, hcol2 = st.columns([1, 1])
        with hcol1:
            st.metric("Total Flagged Inconsistencies", len(audit_records))
            if rule_violations_count:
                vdf = pd.DataFrame(list(rule_violations_count.items()), columns=["Rule", "Violation Count"]).sort_values("Violation Count", ascending=False)
                fig_rules = px.bar(vdf, x="Violation Count", y="Rule", orientation="h", title="Violations Detected by Rule Type")
                fig_rules.update_layout(height=350, margin=dict(l=0, r=0, t=30, b=0))
                st.plotly_chart(fig_rules, use_container_width=True)
                
        with hcol2:
            st.markdown("##### 📋 Defensive Rules Checked:")
            st.markdown(
                r"""
                - **Rule 1:** Non-technical title claiming excessive AI skills ($\ge 8$).
                - **Rule 2:** High AI skill claims with under 2 years total experience.
                - **Rule 3:** Claimed retrieval/vector stack with zero applied AI project evidence.
                - **Rule 4:** Low completeness with zero developer activity.
                - **Rule 5:** Unrealistic number of expert skills for junior profile.
                - **Rule 6:** Cumulative skill durations exceed possible career tenure.
                - **Rule 7:** Inverted education timeline (start year > end year).
                - **Rule 8:** Career duration at company exceeds company existence date.
                - **Rule 9:** AI/ML title with almost no reported AI skills.
                - **Rule 10:** Fake superstar profile (high skills, 0 GitHub, low completeness).
                - **Rule 11:** Frequent short-term job hopping.
                """
            )
            
        st.markdown("---")
        st.markdown("##### 🚨 Penalized Candidates Audit Table")
        if audit_records:
            st.dataframe(pd.DataFrame(audit_records), use_container_width=True)
        else:
            st.success("No honeypots or inconsistent profiles detected in the current ranked selection.")

# =========================================================================
# TAB 5: TALENT POOL ANALYTICS
# =========================================================================
with tab_analytics:
    if not st.session_state.ranked_results:
        st.info("Run candidate ranking to view talent pool analytics.")
    else:
        st.markdown("#### 📊 Talent Pool Distribution & Insights")
        
        ranked_list = st.session_state.ranked_results
        analytics_data = []
        for c in ranked_list:
            raw = raw_candidates_map.get(c["candidate_id"], {})
            cf = c.get("candidate_features", {})
            prof = raw.get("profile", {})
            analytics_data.append({
                "score": c["score"],
                "experience": prof.get("years_of_experience", 0),
                "notice_period": cf.get("notice_period", 90),
                "github_score": cf.get("github_score", 0),
                "ai_skills": cf.get("ai_skill_count", 0),
                "retrieval_skills": cf.get("retrieval_skill_count", 0),
                "company": prof.get("current_company", "Other"),
                "is_product": cf.get("product_company_exp", 0) > 0,
                "is_consulting": cf.get("consulting_only", 0) > 0
            })
        adf = pd.DataFrame(analytics_data)
        
        # Row 1: Score Histogram + Experience vs Score Scatter
        gcol1, gcol2 = st.columns(2)
        with gcol1:
            fig_hist = px.histogram(
                adf,
                x="score",
                nbins=20,
                title="Match Score Distribution",
                color_discrete_sequence=["#059669"]
            )
            fig_hist.update_layout(margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig_hist, use_container_width=True)
            
        with gcol2:
            fig_scatter = px.scatter(
                adf,
                x="experience",
                y="score",
                color="notice_period",
                size="ai_skills",
                hover_data=["company"],
                title="Experience vs Match Score (Colored by Notice Period)",
                color_continuous_scale="Blues"
            )
            fig_scatter.update_layout(margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig_scatter, use_container_width=True)
            
        # Row 2: Notice Period & Company Background
        gcol3, gcol4 = st.columns(2)
        with gcol3:
            notice_counts = adf["notice_period"].value_counts().reset_index()
            notice_counts.columns = ["Notice Period (Days)", "Count"]
            fig_notice = px.pie(
                notice_counts,
                names="Notice Period (Days)",
                values="Count",
                title="Notice Period Distribution",
                hole=0.4
            )
            fig_notice.update_layout(margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig_notice, use_container_width=True)
            
        with gcol4:
            comp_types = pd.DataFrame([
                {"Category": "Product / AI Companies", "Count": adf["is_product"].sum()},
                {"Category": "Consulting Only", "Count": adf["is_consulting"].sum()},
                {"Category": "General Tech / Other", "Count": len(adf) - adf["is_product"].sum() - adf["is_consulting"].sum()}
            ])
            fig_comp = px.bar(
                comp_types,
                x="Category",
                y="Count",
                color="Category",
                title="Company Background Breakdown",
                color_discrete_sequence=["#10B981", "#EF4444", "#3B82F6"]
            )
            fig_comp.update_layout(margin=dict(l=0, r=0, t=30, b=0), showlegend=False)
            st.plotly_chart(fig_comp, use_container_width=True)
