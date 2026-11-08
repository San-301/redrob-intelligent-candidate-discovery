# Product User Manual: Redrob Intelligent Candidate Discovery

A comprehensive, non-technical guide to operating the **Redrob Intelligent Candidate Discovery & Ranking Platform**.

---

## 🚀 Quick Start (Under 1 Minute)

1. Launch the application in your terminal:
   ```bash
   streamlit run app.py
   ```
2. In the left sidebar:
   - Click **"⚡ Sample"** and hit **"⚡ Load Benchmark Sample Dataset (50 Profiles)"** (or upload your `candidates.jsonl`).
   - Select your desired **Job Description Preset** (e.g., *Redrob Challenge: Senior Retrieval & Ranking Engineer*).
3. Click the primary button: **"🚀 Run Candidate Discovery & Ranking"**.
4. Explore your ranked candidates in the **Candidate Discovery & Ranking** tab!

---

## 🧭 Navigation & Core Features Overview

```text
┌────────────────────────────────────────────────────────────────────────┐
│ 1. Sidebar: Ingestion & Settings                                      │
│    ├── Ingestion: Upload File | Local Path | Benchmark Sample          │
│    ├── Job Description: Choose Preset or Type Custom JD                │
│    └── Parameters: Top-K Slider & Strict Honeypot Quarantine           │
└────────────────────────────────────┬───────────────────────────────────┘
                                     │
                                     ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 2. Main Workspace: 5 Dedicated Recruiter Tabs                          │
│    ├── 🎯 Candidate Discovery & Ranking  (Main list, filters, exports) │
│    ├── 👤 Candidate Deep Dive            (Full profile dossier)        │
│    ├── ⚖️ Candidate Comparison Lab       (Side-by-side head-to-head)   │
│    ├── 🛡️ Honeypot & Risk Lab            (Anti-fraud & audit checks)   │
│    └── 📊 Talent Pool Analytics          (Score & talent visual charts)│
└────────────────────────────────────────────────────────────────────────┘
```

---

## 📥 Step 1: Candidate Data Ingestion

The platform offers three flexible ways to load candidate datasets:

| Tab | When to Use | How It Works |
| :--- | :--- | :--- |
| **📁 Upload File** | You have a file on your device | Drag-and-drop any `.jsonl` or `.json` file. Supports files up to **1 GB** (including the official 465 MB hackathon dataset). |
| **💻 Local Path** | Fastest for 400 MB+ files | Point directly to a file on your disk (e.g. `data/raw/candidates.jsonl`) and click **"📂 Load from Local Disk"**. Loads in seconds without browser upload delay. |
| **⚡ Sample** | Quick demonstration or testing | Click **"⚡ Load Benchmark Sample Dataset"** to immediately load 50 realistic candidate profiles (Tier-1 matches, consulting profiles, and honeypots). |

---

## 📋 Step 2: Setting the Job Description & Parameters

### 1. Job Description Presets
- **Redrob Challenge: Senior Retrieval & Ranking Engineer:** Tailored to the official competition specification (Dense vector search, BM25, embeddings, NDCG/MRR, production ML).
- **Generative AI & LLM Systems Engineer:** Tailored to RAG architectures, LLM fine-tuning (LoRA, QLoRA), and vector databases.
- **Search & Relevance Platform Architect:** Tailored to large-scale distributed search infrastructure (Elasticsearch, OpenSearch, Vespa).
- **Custom Job Description:** Paste any job description text, set minimum/maximum experience years, and specify required skills.

### 2. Execution Parameters
- **Top-K Slider:** Choose how many candidates to rank (e.g., top 10, 50, or 100).
- **Strict Honeypot Quarantine:** When enabled, candidates exhibiting suspicious anomalies or fraud flags are automatically removed from the final recommendations.

---

## 🎯 Step 3: Reviewing Ranked Matches (Discovery Tab)

Once ranking completes, the **Candidate Discovery & Ranking** tab displays the ranked pool.

### Understanding Candidate Cards:
- **Rank Badge:** Distinct visual indicator (`#1` Gold, `#2` Silver, `#3` Bronze, `#4+` Slate).
- **Candidate Title & Pedigree:** Displays current title, company, years of experience, and Candidate ID.
- **Match Score & Tier:** High-contrast calibrated score (e.g., `0.9780`) and tier badge:
  - `★ Top Tier Match` (Score: 0.940 – 0.980)
  - `Strong Match` (Score: 0.850 – 0.939)
  - `Good Match` (Score: 0.780 – 0.849)
  - `Adjacent Profile` (Score: 0.740 – 0.779)
  - `⚠️ Risk Flagged` (Flagged by honeypot defense)
- **AI Recommendation Callout:** A human-readable, deterministic explanation of why this candidate was selected.
- **Skill Badges:** Quick visual pills showing verified matches (`✓ retrieval`, `✓ semantic search`).
- **Availability Signals:** Notice period badge (`⏱ 30d Notice`), Open to Work indicator, and GitHub activity score.
- **Expandable Details:** Click **"🔍 View Profile Details & Career History"** inside any card to inspect their background on demand without leaving the list.

### Filter & Search Toolbar:
- **Search Box:** Filter candidates in real-time by title, company, or Candidate ID.
- **Min Match Score Slider:** Show only candidates above a certain score threshold.
- **Max Notice Period Filter:** Filter for candidates available within $\le 30$ days, $\le 60$ days, or $\le 90$ days.
- **Checkboxes:** Toggle **"Open to Work Only"** or **"Exclude Risk Flagged"**.
- **Display Views:** Toggle between **Card View (Detailed)** and **Interactive Table View**.
- **Pagination:** Select **Per Page** (`10`, `20`, `50`, or `All`) to avoid scrolling fatigue.

---

## 👤 Step 4: Candidate Deep Dive

Use this tab when you need an in-depth audit of a specific candidate:
1. Select any candidate from the dropdown list.
2. **Score Contribution Chart:** A visual horizontal bar chart showing exactly how much each signal (Retrieval, Experience, Production ML, Company, etc.) contributed to their score.
3. **Anti-Fraud Audit:** Confirms whether the profile passed all 11 honeypot checks or shows the exact triggered penalties.
4. **Career History Timeline:** Chronological breakdown of their past companies, roles, durations, and project descriptions.
5. **Skills Inventory:** Grouped by claimed proficiency (*Expert*, *Advanced*, *Intermediate*).
6. **Raw JSON Viewer:** Inspect the exact original JSON record for technical verification.

---

## ⚖️ Step 5: Candidate Comparison Lab

Compare 2 or 3 shortlisted candidates head-to-head:
1. Open the **Candidate Comparison Lab** tab.
2. Select 2 or 3 candidate IDs from the multi-select box.
3. View side-by-side comparative cards covering:
   - Rank & Calibrated Match Score
   - Years of Experience & Company Background
   - Notice Period & Immediate Availability
   - AI and Retrieval Skill Counts
   - GitHub Developer Score & Recruiter Response Rate
   - Honeypot Risk Status & AI Evaluation Reasoning

---

## 🛡️ Step 6: Honeypot & Fraud Defense Lab

The dataset contains synthetic or deliberately misleading profiles designed to test recruiter systems. This tab serves as your fraud audit center:
- **KPI Metrics:** Total flagged profiles and total penalties applied.
- **Violation Breakdown Chart:** Visual bar chart showing which rules were violated most frequently across the dataset.
- **Checked Defensive Rules:**
  - *Rule 1:* Non-technical title claiming excessive AI skills ($\ge 8$).
  - *Rule 2:* High AI skill claims with under 2 years total experience.
  - *Rule 3:* Claimed AI stack lacking retrieval experience.
  - *Rule 4:* Low completeness with zero developer activity.
  - *Rule 5:* Unrealistic number of expert skills for junior profile.
  - *Rule 6:* Cumulative skill durations exceed possible career tenure.
  - *Rule 7:* Inverted education timeline (start year > end year).
  - *Rule 8:* Career duration at company exceeds company existence date.
  - *Rule 9:* AI/ML title with almost no reported AI skills.
  - *Rule 10:* Fake superstar profile (high skills, 0 GitHub, low completeness).
  - *Rule 11:* Frequent short-term job hopping.
- **Audit Table:** Full table of all penalized candidates with the specific triggered reasons.

---

## 📊 Step 7: Talent Pool Analytics

Provides executive-level charts summarizing the candidate pool:
- **Match Score Distribution:** Histogram illustrating candidate quality tiers.
- **Experience vs. Match Score:** Scatter plot showing how seniority correlates with ranking score (colored by notice period).
- **Notice Period Breakdown:** Donut chart showing candidate availability across the top matches.
- **Company Pedigree:** Bar chart breaking down candidates from Tier-1 Product/AI startups versus Consulting backgrounds.

---

## 📥 Step 8: One-Click Data Exports

Located at the top-right of the **Candidate Discovery & Ranking** tab:
1. **📥 Download Official Submission CSV:**
   - Produces `submission.csv` strictly adhering to the Hackathon submission specification:
   - Columns: `candidate_id, rank, score, reasoning`
   - Verified for non-increasing scores, unique candidate IDs, and exact rank numbering (1–100).
2. **📊 Download Comprehensive Report CSV:**
   - Produces `candidate_discovery_report.csv` containing all computed feature values, verified skills, notice periods, and honeypot flags for internal hiring team review.
