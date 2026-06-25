# Redrob Intelligent Candidate Discovery

## Overview

This project is a production-style AI recruiter system developed for the Redrob Intelligent Candidate Discovery & Ranking Challenge.

The system ranks candidates from a large candidate pool by combining:

* Candidate profile understanding
* Feature engineering
* Hybrid retrieval and ranking
* Behavioral signals
* Honeypot detection
* Explainable AI reasoning

The objective is to identify the most suitable candidates for a given job description while maintaining production constraints such as low latency, CPU-only execution, and reproducibility.

---

## Key Features

* Hybrid candidate retrieval and ranking
* AI/ML skill extraction
* Retrieval and ranking experience detection
* Production ML experience identification
* Evaluation framework detection (NDCG, MRR, MAP, A/B Testing)
* Behavioral signal integration
* Honeypot candidate detection
* Explainable ranking reasons
* Deterministic ranking with reproducible results

---

## Architecture

Candidate JSONL

      ↓

CandidateParser

      ↓

FeatureBuilder

      ↓

HoneypotDetector

      ↓

CandidateScorer

      ↓

CandidateRanker

      ↓

ReasonGenerator

      ↓

Submission CSV

---

## Repository Structure

```text
src/
├── preprocessing/
├── features/
├── ranking/
├── retrieval/
├── reasoning/
├── validation/

rank.py
requirements.txt
README.md
```

## Installation

```bash
pip install -r requirements.txt
```

## Generate Submission

```bash
python rank.py --candidates data/raw/candidates.jsonl --out submission.csv
```

## Runtime Characteristics

* CPU-only execution
* No external API calls
* Runtime: ~30 seconds for 100K candidates
* Memory usage: <16 GB

## Validation

```bash
python validate_final_submission.py
```

## Competition Constraints

* No GPU usage during ranking
* No network/API calls during ranking
* Ranking runtime under 5 minutes
* Deterministic and reproducible pipeline
