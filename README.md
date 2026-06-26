# Redrob Intelligent Candidate Discovery

## Overview

Redrob Intelligent Candidate Discovery is a production-grade AI recruiter system developed for the **Redrob Intelligent Candidate Discovery & Ranking Challenge**.

The system identifies and ranks the top candidates for a given Job Description by combining semantic profile understanding, feature engineering, behavioral signals, and explainable AI reasoning.

The ranking pipeline is designed to mimic real-world recruiting systems while satisfying strict production constraints such as low latency, CPU-only execution, reproducibility, and scalability.

---

## Key Features

* Intelligent candidate ranking for large candidate pools (100K+ candidates)
* Hybrid retrieval and ranking architecture
* AI/ML skill extraction and profiling
* Retrieval, search, and ranking experience detection
* Production ML experience identification
* Behavioral signal integration
* Product company and AI company experience modeling
* Honeypot candidate detection and penalization
* Explainable ranking with human-readable reasoning
* Deterministic and reproducible ranking pipeline

---

## System Architecture

```text
Candidate JSONL
        │
        ▼
CandidateParser
        │
        ▼
FeatureBuilder
        │
        ▼
HoneypotDetector
        │
        ▼
Semantic Retrieval
        │
        ▼
CandidateScorer
        │
        ▼
CandidateRanker
        │
        ▼
ReasonGenerator
        │
        ▼
Submission CSV
```

---

## Repository Structure

```text
src/
├── embeddings/
├── features/
├── preprocessing/
├── ranking/
├── reasoning/
├── retrieval/
├── utils/
├── validation/

rank.py
requirements.txt
README.md
```

---

## Ranking Signals

The final ranking score combines multiple signals:

* Experience relevance
* Title relevance
* Retrieval and search expertise
* Evaluation framework knowledge
* AI/ML experience
* Production deployment evidence
* Product company background
* Behavioral engagement signals
* Recruiter interaction signals
* Open-to-work status
* Leadership signals
* Honeypot and inconsistency penalties

---

## Honeypot Detection

The dataset contains intentionally misleading profiles (honeypots). To improve ranking quality, the system implements explicit profile consistency checks.

Detected inconsistencies include:

* Unrealistic skill inflation
* Suspicious experience-to-skill ratios
* Research-heavy profiles with limited production evidence
* Profile inconsistencies across career history and claimed expertise

Candidates exhibiting suspicious behavior receive penalties during ranking, reducing the likelihood of honeypots appearing in the final Top-100.

---

## Runtime Characteristics

| Constraint    | Value       |
| ------------- | ----------- |
| Runtime       | ~30 seconds |
| Compute       | CPU Only    |
| GPU Usage     | No          |
| Network Calls | None        |
| Memory        | <16 GB      |

---

## Validation Framework

The project includes a comprehensive validation framework to ensure strict compliance with the official hackathon submission specification.

Validation checks include:

* Exactly 100 ranked candidates
* Unique candidate IDs
* Unique rank values (1-100)
* Monotonically non-increasing scores
* Duplicate reasoning detection
* Submission format verification
* Reasoning diversity analysis
* Final submission integrity checks

Validation scripts:

```bash
python validate_submission.py
python validate_final_submission.py
```

The final validator was developed based on the official hackathon submission specification and additionally performs custom quality checks to improve submission robustness.

---

## Dataset Setup

Place the official hackathon dataset in:

```text
data/raw/candidates.jsonl
```

The dataset is not included in this repository because it is distributed separately as part of the official hackathon bundle.

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Generate Submission

```bash
python rank.py --candidates data/raw/candidates.jsonl --out submission.csv
```

---

## Validate Submission

```bash
python validate_final_submission.py
```

---

## Explainable AI Reasoning

Every ranked candidate is accompanied by a human-readable explanation.

Reasoning generation considers:

* Years of experience
* Current title relevance
* Retrieval and ranking expertise
* Production ML evidence
* AI/ML experience
* Behavioral signals
* Recruiter engagement
* Potential concerns and risk factors

The generated explanations are:

* Candidate-specific
* Deterministic
* Non-hallucinatory
* Rank-aware
* Aligned with competition evaluation criteria

---

## Reproducibility

The ranking pipeline is fully deterministic and reproducible.

* No external API calls
* No hosted LLM dependencies
* CPU-only execution
* Deterministic tie-breaking
* Reproducible ranking outputs

---

## Additional Engineering Considerations

Several engineering practices were adopted to improve production readiness:

* Deterministic ranking with tie-breaking
* CPU-only execution for scalability
* Hybrid retrieval architecture
* Modular pipeline design
* Feature-based scoring for low latency
* Local experimentation and iterative refinement
* Complete offline execution without external APIs

The repository represents the final production-ready version of the system after extensive local experimentation, profiling, and iterative optimization.

---

## Competition Constraints

This solution adheres to all competition constraints:

* CPU-only ranking
* Runtime under 5 minutes
* No network/API calls during ranking
* No GPU usage during ranking
* Fully reproducible pipeline

---

## Authors

**Builder of AI Team**

Developed for the **Redrob Intelligent Candidate Discovery & Ranking Challenge**.
