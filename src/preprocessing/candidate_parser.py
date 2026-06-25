# src/preprocessing/candidate_parser.py
from typing import Dict

class CandidateParser:

    CONSULTING_COMPANIES = {
        "TCS",
        "Infosys",
        "Wipro",
        "Cognizant",
        "Accenture",
        "Capgemini",
        "HCL",
        "Tech Mahindra",
        "Mphasis"
    }

    PRODUCT_COMPANIES = {
        "Google",
        "Amazon",
        "Meta",
        "Microsoft",
        "LinkedIn",
        "Uber",
        "Zomato",
        "Swiggy",
        "Flipkart",
        "PhonePe",
        "CRED",
        "Razorpay",
        "Ola",
        "Meesho",
        "Freshworks",
        "Zoho",
        "Dream11",
        "Nykaa",
        "Paytm"
    }

    AI_COMPANIES = {
        "Observe.AI",
        "Yellow.ai",
        "Sarvam AI",
        "Krutrim",
        "Haptik",
        "Mad Street Den",
        "Rephrase.ai",
        "Wysa",
        "Aganitha",
        "Verloop.io"
    }

    AI_SKILLS = {
        "llms",
        "rag",
        "embeddings",
        "vector search",
        "semantic search",
        "information retrieval",
        "retrieval",
        "recommendation systems",
        "sentence transformers",
        "hugging face transformers",
        "langchain",
        "pinecone",
        "faiss",
        "qdrant",
        "weaviate",
        "milvus",
        "bm25",
        "opensearch",
        "elasticsearch",
        "lora",
        "qlora",
        "peft",
        "fine-tuning llms",
        "machine learning",
        "deep learning",
        "nlp",
        "tensorflow",
        "pytorch",
        "mlops",
        "openai",
        "anthropic",
        "cohere",
        "gemini",
        "claude",
        "reranker",
        "cross encoder",
        "cross-encoder",
        "bge",
        "e5",
        "colbert",
        "retriever"
    }

    RETRIEVAL_SKILLS = {
        "retrieval",
        "semantic search",
        "vector search",
        "embeddings",
        "information retrieval",
        "recommendation systems",
        "faiss",
        "pinecone",
        "qdrant",
        "weaviate",
        "milvus",
        "bm25",
        "elasticsearch",
        "opensearch",
        "retriever"
    }

    EVAL_TERMS = {
        "ndcg",
        "mrr",
        "map",
        "a/b testing",
        "ab testing",
        "offline benchmark",
        "evaluation"
    }

    STRONG_AI_TITLES = {
        "ai engineer",
        "ml engineer",
        "machine learning engineer",
        "search engineer",
        "recommendation systems engineer",
        "recommendation engineer",
        "nlp engineer",
        "data scientist",
        "applied scientist",
        "ai research engineer"
        "machine learning scientist",
        "applied ml engineer",
        "senior machine learning engineer",
        "staff machine learning engineer",
        "principal machine learning engineer",
        "recommendation scientist",
        "relevance engineer",
        "ranking engineer",
        "search relevance engineer",
    }

    MEDIUM_AI_TITLES = {
        "data engineer",
        "backend engineer",
        "software engineer",
        "platform engineer"
    }

    NON_AI_TITLES = {
            "graphic designer",
            "marketing manager",
            "customer support",
            "accountant",
            "hr manager",
            "sales executive",
            "civil engineer",
            "mechanical engineer",
            "operations manager",
            "content writer",
            "project manager",
            "business analyst",
            "sales manager",
            "marketing analyst",
            "finance analyst",
            "hr business partner"
        }

    PRODUCT_COMPANIES_LOWER = {
        c.lower() for c in PRODUCT_COMPANIES
    }

    AI_COMPANIES_LOWER = {
        c.lower() for c in AI_COMPANIES
    }

    CONSULTING_COMPANIES_LOWER = {
        c.lower() for c in CONSULTING_COMPANIES
    }
    
    @staticmethod
    def normalize_text(text):

        if text is None:
            return ""

        return str(text).lower().strip()


    @staticmethod
    def normalize_title(title):

        title = CandidateParser.normalize_text(title)

        prefixes = [
            "senior ",
            "sr ",
            "lead ",
            "staff ",
            "principal ",
            "junior ",
            "jr "
        ]

        for p in prefixes:
            title = title.replace(p, "")

        return title.strip()

    @staticmethod
    def clean_github_score(score):

        if score is None:
            return 0

        if score < 0:
            return 0

        return min(score, 100)


    @staticmethod
    def clean_notice_period(days):

        if days is None:
            return 90

        return max(
            0,
            min(days, 180)
        )


    @staticmethod
    def clean_percentage(value):

        if value is None:
            return 0

        return max(
            0,
            min(value, 1.0)
        )


    @staticmethod
    def clean_profile_completeness(score):

        if score is None:
            return 0

        return max(
            0,
            min(score, 100)
        )

    def parse(self, candidate: Dict) -> Dict:

        profile = candidate.get("profile", {})
        career = candidate.get("career_history", [])
        skills = candidate.get("skills", [])
        signals = candidate.get("redrob_signals", {})

        skill_names = {

            str(
                s.get("name", "")
            ).lower().strip()

            for s in skills

            if s.get("name")
        }

        skill_text = " ".join(skill_names)

        current_title = self.normalize_title(
            profile.get(
                "current_title",
                ""
            )
        )

        summary = self.normalize_text(
            profile.get(
                "summary",
                ""
            )
        )
    
        headline = self.normalize_text(
            profile.get(
                "headline",
                ""
            )
        )

        current_company = self.normalize_text(
            profile.get(
                "current_company",
                ""
            )
        )

        career_text = " ".join(

            self.normalize_text(
                job.get(
                    "description",
                    ""
                )
            )

            for job in career
        )

        full_text = (
            current_title
            + " "
            + headline
            + " "
            + summary
            + " "
            + career_text
            + " "
            + skill_text
        )

        ai_skill_count = sum(
            skill in full_text
            for skill in self.AI_SKILLS
        )

        retrieval_skill_count = sum(
            skill in full_text
            for skill in self.RETRIEVAL_SKILLS
        )

        evaluation_skill_count = sum(
            term in full_text
            for term in self.EVAL_TERMS
        )

        retrieval_experience = int(
            retrieval_skill_count > 0
        )

        title_strength = 0.0

        for title in self.STRONG_AI_TITLES:
            if title in current_title:
                title_strength = 1.0
                break

        if title_strength == 0:
            for title in self.MEDIUM_AI_TITLES:
                if title in current_title:
                    title_strength = 0.6
                    break


        consulting_jobs = 0
        product_company_exp = 0
        ai_company_exp = 0

        if any(
            p in current_company
            for p in self.PRODUCT_COMPANIES_LOWER):
                product_company_exp += 1

        if any(
            a in current_company
            for a in self.AI_COMPANIES_LOWER
        ):
            ai_company_exp += 1


        for job in career:

            company = self.normalize_text(
                job.get(
                    "company",
                    ""
                )
            )

            if any(
                c in company
                for c in self.CONSULTING_COMPANIES_LOWER
            ):
                consulting_jobs += 1

            if any(
                p in company
                for p in self.PRODUCT_COMPANIES_LOWER
            ):
                product_company_exp += 1

            if any(
                a in company
                for a in self.AI_COMPANIES_LOWER
            ):
                ai_company_exp += 1
                
        consulting_background = int(
        consulting_jobs > 0
        )

        consulting_only = int(
            len(career) > 0
            and consulting_jobs == len(career)
        )

        ai_months = 0

        for skill in skills:

            if (
                skill.get(
                    "name",
                    ""
                ).lower()
                in self.AI_SKILLS
            ):
                ai_months += skill.get(
                    "duration_months",
                    0
                )

        leadership_score = 0

        leadership_words = [
            "led",
            "managed",
            "mentor",
            "mentored",
            "team lead",
            "hiring",
            "owned"
        ]

        for word in leadership_words:

            if word in full_text:
                leadership_score += 1

        leadership_score = min(
            leadership_score / 5,
            1.0
        )

        # Real AI work from career history
        career_ai_terms = [
            "retrieval",
            "ranking",
            "recommendation",
            "search",
            "embeddings",
            "vector",
            "semantic search",
            "information retrieval",
            "llm",
            "transformer",
            "fine tuning",
            "fine-tuning",
            "machine learning",
            "deep learning",
            "rag",
            "reranking",
            "re-ranking",
            "ndcg",
            "mrr",
            "map",
            "a/b",
            "ab test",
            "experiment",
            "online evaluation",
            "offline evaluation"
        ]

        career_ai_hits = sum(
            term in full_text
            for term in career_ai_terms
        )

        career_ai_score = min(
            career_ai_hits / 10,
            1.0
        )

        # Evaluation framework experience
        evaluation_experience = int(
            evaluation_skill_count > 0
        )

        # JD explicitly rejects these profiles
        

        non_ai_title_penalty = int(
            any(
                title in current_title
                for title in self.NON_AI_TITLES
            )
        )

        github_score = self.clean_github_score(
            signals.get(
                "github_activity_score",
                0
            )
        )

        notice_period = self.clean_notice_period(
            signals.get(
                "notice_period_days",
                90
            )
        )

        response_rate = self.clean_percentage(
            signals.get(
                "recruiter_response_rate",
                0
            )
        )

        interview_completion = self.clean_percentage(
            signals.get(
                "interview_completion_rate",
                0
            )
        )

        production_terms = [
        "production",
        "deployed",
        "deployment",
        "scale",
        "users",
        "real users",
        "ab testing",
        "a/b testing",
        "monitoring",
        "latency",
        "index",
        "online",
        "offline",
        "experimentation"
        ]


        profile_completeness = (
            self.clean_profile_completeness(
                signals.get(
                    "profile_completeness_score",
                    0
                )
            )
        )

        production_hits = sum(
            term in full_text
            for term in production_terms
        )

        production_score = min(
            production_hits / 6,
            1.0
        )
    
        research_terms = [
            "phd",
            "research scientist",
            "research fellow",
            "paper",
            "publication",
            "academic"
        ]

        research_hits = sum(
            1
            for term in research_terms
            if term in full_text
        )

        pure_research_penalty = int(
            research_hits >= 3
            and production_score < 0.2
        )

        suspicious_skills = 0

        for skill in skills:

            prof = self.normalize_text(
                skill.get(
                    "proficiency",
                    ""
                )
            )

            months = skill.get(
                "duration_months",
                0
            )

            if (
                prof == "expert"
                and months < 6
            ):
                suspicious_skills += 1
                
        last_active = signals.get(
            "last_active_date",
            ""
        )

        recent_activity_score = 0.0

        if last_active:

            if last_active >= "2026-05-25":
                recent_activity_score = 1.0

            elif last_active >= "2026-05-01":
                recent_activity_score = 0.8

            elif last_active >= "2026-03-01":
                recent_activity_score = 0.5

            elif last_active >= "2025-12-01":
                recent_activity_score = 0.2

        return {

            "candidate_id":
                candidate["candidate_id"],

            "years_experience":
                profile.get(
                    "years_of_experience",
                    0
                ),

            "current_title":
                profile.get(
                    "current_title",
                    ""
                ),

            "current_company":
                profile.get(
                    "current_company",
                    ""
                ),

            "current_industry":
                profile.get(
                    "current_industry",
                    ""
                ),

            "title_strength":
                title_strength,

            "ai_skill_count":
                ai_skill_count,

            "retrieval_skill_count":
                retrieval_skill_count,

            "evaluation_skill_count":
                evaluation_skill_count,

            "retrieval_experience":
                retrieval_experience,

            "consulting_background":
                consulting_background,

            "consulting_only":
                consulting_only,

            "product_company_exp":
                product_company_exp,

            "ai_company_exp":
                ai_company_exp,

            "ai_months":
                ai_months,

            "leadership_score":
                leadership_score,

            "github_score":
                github_score,

            "response_rate":
                response_rate,

            "interview_completion":
                interview_completion,

            "open_to_work":
                int(
                    signals.get(
                        "open_to_work_flag",
                        False
                    )
                ),

            "notice_period":
                notice_period,

            "saved_by_recruiters":
                signals.get(
                    "saved_by_recruiters_30d",
                    0
                ),

            "search_appearance":
                signals.get(
                    "search_appearance_30d",
                    0
                ),

            "profile_completeness":
                profile_completeness,

            "career_ai_hits":
                career_ai_hits,

            "career_ai_score":
                career_ai_score,

            "evaluation_experience":
                evaluation_experience,

            "non_ai_title_penalty":
                non_ai_title_penalty,

            "recent_activity_score":
                recent_activity_score,

            "production_score":
                production_score,
            
            "pure_research_penalty":
                pure_research_penalty,
            
            "suspicious_skill_count":
                suspicious_skills,

            "career_length": len(career)
        }
