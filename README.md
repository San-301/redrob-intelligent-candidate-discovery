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
├── features/
├── preprocessing/
├── ranking/
├── reasoning/
├── retrieval/
├── validation/

data/
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
* Honeypot and inconsistency penalties

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

## Reproducibility

The ranking pipeline is fully deterministic and reproducible.

* No external API calls
* No hosted LLM dependencies
* CPU-only execution
* Deterministic tie-breaking
* Reproducible ranking outputs

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

Builder of AI Team

Developed for the Redrob Intelligent Candidate Discovery & Ranking Challenge.
