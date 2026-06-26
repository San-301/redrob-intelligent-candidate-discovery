import pandas as pd
import json

# Load top 100 ids from submission
submission = pd.read_csv("team_Builder_of_AI.csv")

top_ids = set(submission["candidate_id"])

stats = {
    "retrieval": 0,
    "evaluation": 0,
    "product_company": 0,
    "ai_company": 0,
    "open_to_work": 0,
    "notice_gt_90": 0,
    "total": 0
}

sample_profiles = []

with open("data/raw/candidates.jsonl", "r", encoding="utf-8") as f:

    for line in f:

        candidate = json.loads(line)

        cid = candidate["candidate_id"]

        if cid not in top_ids:
            continue

        stats["total"] += 1

        profile = candidate.get("profile", {})
        skills = candidate.get("skills", [])
        signals = candidate.get("redrob_signals", {})

        skill_text = " ".join(
            s.get("name", "").lower()
            for s in skills
        )

        if any(k in skill_text for k in [
            "retrieval",
            "search",
            "embeddings",
            "faiss",
            "qdrant",
            "pinecone",
            "recommendation"
        ]):
            stats["retrieval"] += 1

        if any(k in skill_text for k in [
            "ndcg",
            "mrr",
            "map",
            "evaluation"
        ]):
            stats["evaluation"] += 1

        career = candidate.get("career_history", [])

        companies = " ".join(
            c.get("company", "").lower()
            for c in career
        )

        if any(c in companies for c in [
            "google",
            "amazon",
            "meta",
            "microsoft",
            "uber",
            "linkedin",
            "flipkart"
        ]):
            stats["product_company"] += 1

        if any(c in companies for c in [
            "observe.ai",
            "yellow.ai",
            "sarvam",
            "haptik"
        ]):
            stats["ai_company"] += 1

        if signals.get("open_to_work_flag"):
            stats["open_to_work"] += 1

        if signals.get("notice_period_days", 0) > 90:
            stats["notice_gt_90"] += 1

        sample_profiles.append({
            "candidate_id": cid,
            "title": profile.get("current_title"),
            "exp": profile.get("years_of_experience")
        })

print("\n========== TOP-100 ANALYSIS ==========\n")

for k, v in stats.items():

    if k == "total":
        continue

    print(
        f"{k}: {v}/{stats['total']} "
        f"({100*v/stats['total']:.1f}%)"
    )

print("\nSample Top Candidates:\n")

for p in sample_profiles[:20]:
    print(
        f"{p['candidate_id']} | "
        f"{p['title']} | "
        f"{p['exp']} yrs"
    )