# src/sample_data.py
"""
Sample candidate dataset generator for testing and live demonstration
of the Redrob Intelligent Candidate Discovery platform.
"""
from typing import List, Dict

def get_sample_candidates() -> List[Dict]:
    """
    Returns 50 realistic, diverse candidate profiles covering:
    - Tier-1 Retrieval & Search Experts (Top matches)
    - Applied ML / Recommendation Engineers (Strong matches)
    - General Backend / Data Engineers (Good / Adjacent matches)
    - Consulting / IT Services profiles (Penalized for consulting-only)
    - Intentional Honeypot profiles (Triggering fraud & consistency rules)
    """
    candidates = [
        # --- Top-Tier Retrieval & Ranking Engineers ---
        {
            "candidate_id": "CAND_0001001",
            "profile": {
                "current_title": "Senior Machine Learning Engineer",
                "current_company": "Observe.AI",
                "current_industry": "Artificial Intelligence",
                "years_of_experience": 7.0,
                "headline": "Search & Ranking Engineer | Semantic Search, Vector DBs, Production RecSys",
                "summary": "7+ years architecting dense retrieval and neural ranking systems at scale. Led semantic search overhaul using FAISS, embeddings, and cross-encoders. Proven track record deploying models to 10M+ users with low latency and measurable NDCG gains."
            },
            "career_history": [
                {
                    "title": "Senior ML Engineer",
                    "company": "Observe.AI",
                    "duration_months": 36,
                    "description": "Led team of 4 engineers building production vector search and retrieval augmented generation (RAG) platform. Implemented dense retrieval with embeddings and FAISS index, improving NDCG@10 by 16% in production A/B testing."
                },
                {
                    "title": "Machine Learning Engineer",
                    "company": "Flipkart",
                    "duration_months": 48,
                    "description": "Engineered product recommendation systems and relevance ranking algorithms. Built offline evaluation framework measuring MRR, MAP, and precision. Optimized real-time model inference latency to under 25ms."
                }
            ],
            "skills": [
                {"name": "retrieval", "proficiency": "expert", "duration_months": 54},
                {"name": "semantic search", "proficiency": "expert", "duration_months": 48},
                {"name": "vector search", "proficiency": "expert", "duration_months": 42},
                {"name": "embeddings", "proficiency": "expert", "duration_months": 50},
                {"name": "ranking", "proficiency": "expert", "duration_months": 48},
                {"name": "recommendation systems", "proficiency": "advanced", "duration_months": 40},
                {"name": "faiss", "proficiency": "advanced", "duration_months": 36},
                {"name": "llms", "proficiency": "advanced", "duration_months": 24},
                {"name": "pytorch", "proficiency": "expert", "duration_months": 60},
                {"name": "ndcg", "proficiency": "advanced", "duration_months": 36},
                {"name": "ab testing", "proficiency": "advanced", "duration_months": 36}
            ],
            "education": [
                {"degree": "M.Tech Computer Science", "institution": "IIT Madras", "start_year": 2015, "end_year": 2017},
                {"degree": "B.Tech Computer Science", "institution": "NIT Trichy", "start_year": 2011, "end_year": 2015}
            ],
            "redrob_signals": {
                "github_activity_score": 92.0,
                "notice_period_days": 30,
                "recruiter_response_rate": 0.94,
                "interview_completion_rate": 0.96,
                "open_to_work_flag": True,
                "saved_by_recruiters_30d": 28,
                "search_appearance_30d": 380,
                "profile_completeness_score": 98.0,
                "last_active_date": "2026-06-01",
                "verified_email": True,
                "verified_phone": True,
                "linkedin_connected": True
            }
        },
        {
            "candidate_id": "CAND_0001002",
            "profile": {
                "current_title": "Staff Search Relevance Engineer",
                "current_company": "Swiggy",
                "current_industry": "E-Commerce / Food Delivery",
                "years_of_experience": 8.5,
                "headline": "Search Relevance & Neural Ranking Tech Lead",
                "summary": "Technical lead for consumer search relevance and ranking. Deep expertise in two-stage retrieval (BM25 + Bi-Encoder vector search) and learning-to-rank rerankers. Managed cross-functional ML delivery teams."
            },
            "career_history": [
                {
                    "title": "Staff ML Engineer",
                    "company": "Swiggy",
                    "duration_months": 40,
                    "description": "Owned search ranking and query understanding systems. Implemented hybrid retrieval combining BM25 and vector embeddings in Qdrant. Deployed two-stage ranking pipeline handling 20k QPS."
                },
                {
                    "title": "Senior ML Engineer",
                    "company": "Amazon",
                    "duration_months": 48,
                    "description": "Built candidate retrieval and relevance scoring models for catalog search. Conducted online A/B testing and offline NDCG/MRR evaluation benchmarks."
                }
            ],
            "skills": [
                {"name": "retrieval", "proficiency": "expert", "duration_months": 60},
                {"name": "ranking", "proficiency": "expert", "duration_months": 60},
                {"name": "semantic search", "proficiency": "expert", "duration_months": 48},
                {"name": "embeddings", "proficiency": "expert", "duration_months": 50},
                {"name": "reranker", "proficiency": "expert", "duration_months": 36},
                {"name": "qdrant", "proficiency": "advanced", "duration_months": 24},
                {"name": "bm25", "proficiency": "advanced", "duration_months": 48},
                {"name": "ndcg", "proficiency": "advanced", "duration_months": 40},
                {"name": "mrr", "proficiency": "advanced", "duration_months": 36},
                {"name": "pytorch", "proficiency": "expert", "duration_months": 72}
            ],
            "education": [
                {"degree": "B.Tech Computer Science", "institution": "BITS Pilani", "start_year": 2013, "end_year": 2017}
            ],
            "redrob_signals": {
                "github_activity_score": 85.0,
                "notice_period_days": 15,
                "recruiter_response_rate": 0.90,
                "interview_completion_rate": 0.92,
                "open_to_work_flag": True,
                "saved_by_recruiters_30d": 22,
                "search_appearance_30d": 310,
                "profile_completeness_score": 95.0,
                "last_active_date": "2026-05-28",
                "verified_email": True,
                "verified_phone": True,
                "linkedin_connected": True
            }
        },
        {
            "candidate_id": "CAND_0001003",
            "profile": {
                "current_title": "Machine Learning Engineer",
                "current_company": "Yellow.ai",
                "current_industry": "Conversational AI",
                "years_of_experience": 5.5,
                "headline": "AI Engineer | Vector Search, RAG & LLM Fine-Tuning",
                "summary": "5.5 years designing enterprise NLP and semantic retrieval pipelines. Specialized in FAISS vector indices, embedding fine-tuning, and RAG architectures deployed in production environments."
            },
            "career_history": [
                {
                    "title": "ML Engineer",
                    "company": "Yellow.ai",
                    "duration_months": 32,
                    "description": "Architected conversational search engine with semantic retrieval and LLM reranker. Deployed production vector database serving 5M users."
                },
                {
                    "title": "Junior ML Engineer",
                    "company": "Freshworks",
                    "duration_months": 34,
                    "description": "Engineered ticket classification and automated response recommendation models using transformers and semantic similarity."
                }
            ],
            "skills": [
                {"name": "retrieval", "proficiency": "expert", "duration_months": 40},
                {"name": "embeddings", "proficiency": "expert", "duration_months": 42},
                {"name": "semantic search", "proficiency": "advanced", "duration_months": 36},
                {"name": "faiss", "proficiency": "advanced", "duration_months": 28},
                {"name": "llms", "proficiency": "advanced", "duration_months": 24},
                {"name": "rag", "proficiency": "advanced", "duration_months": 20},
                {"name": "ranking", "proficiency": "intermediate", "duration_months": 24},
                {"name": "python", "proficiency": "expert", "duration_months": 60}
            ],
            "education": [
                {"degree": "B.E. Information Technology", "institution": "Anna University", "start_year": 2016, "end_year": 2020}
            ],
            "redrob_signals": {
                "github_activity_score": 78.0,
                "notice_period_days": 30,
                "recruiter_response_rate": 0.88,
                "interview_completion_rate": 0.85,
                "open_to_work_flag": True,
                "saved_by_recruiters_30d": 18,
                "search_appearance_30d": 240,
                "profile_completeness_score": 92.0,
                "last_active_date": "2026-05-30",
                "verified_email": True,
                "verified_phone": True,
                "linkedin_connected": True
            }
        },
        {
            "candidate_id": "CAND_0001004",
            "profile": {
                "current_title": "AI Engineer",
                "current_company": "Zomato",
                "current_industry": "Consumer Tech",
                "years_of_experience": 6.0,
                "headline": "Lead AI Engineer - Discovery & Search Algorithms",
                "summary": "Specialized in search ranking, personalized candidate recommendation, and vector indexing. Championed A/B testing frameworks and production offline evaluation."
            },
            "career_history": [
                {
                    "title": "Lead AI Engineer",
                    "company": "Zomato",
                    "duration_months": 36,
                    "description": "Led discovery engineering squad. Scaled recommendation systems using hybrid vector search and online A/B testing experimentation."
                },
                {
                    "title": "Machine Learning Engineer",
                    "company": "Ola",
                    "duration_months": 36,
                    "description": "Developed dispatch ranking models and driver allocation algorithms with low-latency constraints."
                }
            ],
            "skills": [
                {"name": "retrieval", "proficiency": "expert", "duration_months": 45},
                {"name": "ranking", "proficiency": "expert", "duration_months": 48},
                {"name": "embeddings", "proficiency": "expert", "duration_months": 40},
                {"name": "recommendation systems", "proficiency": "expert", "duration_months": 50},
                {"name": "vector search", "proficiency": "advanced", "duration_months": 30},
                {"name": "ab testing", "proficiency": "advanced", "duration_months": 36},
                {"name": "ndcg", "proficiency": "advanced", "duration_months": 24}
            ],
            "education": [
                {"degree": "B.Tech Computer Engineering", "institution": "IIT Delhi", "start_year": 2015, "end_year": 2019}
            ],
            "redrob_signals": {
                "github_activity_score": 82.0,
                "notice_period_days": 45,
                "recruiter_response_rate": 0.82,
                "interview_completion_rate": 0.88,
                "open_to_work_flag": False,
                "saved_by_recruiters_30d": 15,
                "search_appearance_30d": 210,
                "profile_completeness_score": 90.0,
                "last_active_date": "2026-05-15",
                "verified_email": True,
                "verified_phone": True,
                "linkedin_connected": True
            }
        },
        {
            "candidate_id": "CAND_0001005",
            "profile": {
                "current_title": "Recommendation Systems Engineer",
                "current_company": "Google",
                "current_industry": "Big Tech",
                "years_of_experience": 8.0,
                "headline": "Senior Software Engineer - Search & Recommendation",
                "summary": "8 years engineering massive-scale retrieval and ranking services. Deep knowledge of metric learning, embedding representations, and multi-task neural rankers."
            },
            "career_history": [
                {
                    "title": "Senior Software Engineer",
                    "company": "Google",
                    "duration_months": 48,
                    "description": "Architected query candidate retrieval systems. Built deep ranking models deployed across distributed serving nodes."
                },
                {
                    "title": "Software Engineer",
                    "company": "Microsoft",
                    "duration_months": 48,
                    "description": "Worked on Bing search relevance and index compression algorithms. Extensively used BM25, semantic search, and NDCG offline benchmarks."
                }
            ],
            "skills": [
                {"name": "retrieval", "proficiency": "expert", "duration_months": 60},
                {"name": "ranking", "proficiency": "expert", "duration_months": 60},
                {"name": "semantic search", "proficiency": "expert", "duration_months": 50},
                {"name": "embeddings", "proficiency": "expert", "duration_months": 55},
                {"name": "recommendation systems", "proficiency": "expert", "duration_months": 50},
                {"name": "ndcg", "proficiency": "expert", "duration_months": 48},
                {"name": "mrr", "proficiency": "expert", "duration_months": 40},
                {"name": "pytorch", "proficiency": "expert", "duration_months": 60}
            ],
            "education": [
                {"degree": "M.S. Computer Science", "institution": "IIT Bombay", "start_year": 2014, "end_year": 2016}
            ],
            "redrob_signals": {
                "github_activity_score": 95.0,
                "notice_period_days": 60,
                "recruiter_response_rate": 0.85,
                "interview_completion_rate": 0.90,
                "open_to_work_flag": True,
                "saved_by_recruiters_30d": 35,
                "search_appearance_30d": 450,
                "profile_completeness_score": 96.0,
                "last_active_date": "2026-05-29",
                "verified_email": True,
                "verified_phone": True,
                "linkedin_connected": True
            }
        },

        # --- Solid Mid-Tier Candidates (Adjacent / Good Match) ---
        {
            "candidate_id": "CAND_0001006",
            "profile": {
                "current_title": "Backend Engineer",
                "current_company": "Razorpay",
                "current_industry": "FinTech",
                "years_of_experience": 6.0,
                "headline": "Backend & Search Infrastructure Engineer",
                "summary": "Specialized in distributed search clusters, Elasticsearch indices, and data pipelines for payment transaction retrieval."
            },
            "career_history": [
                {
                    "title": "Backend Engineer",
                    "company": "Razorpay",
                    "duration_months": 40,
                    "description": "Maintained large Elasticsearch clusters for merchant search and transaction retrieval. Integrated vector similarity search for fraud pattern detection."
                },
                {
                    "title": "Software Engineer",
                    "company": "Paytm",
                    "duration_months": 32,
                    "description": "Built transaction query APIs and indexing services."
                }
            ],
            "skills": [
                {"name": "elasticsearch", "proficiency": "expert", "duration_months": 48},
                {"name": "retrieval", "proficiency": "intermediate", "duration_months": 24},
                {"name": "python", "proficiency": "advanced", "duration_months": 48},
                {"name": "golang", "proficiency": "expert", "duration_months": 40},
                {"name": "opensearch", "proficiency": "intermediate", "duration_months": 18}
            ],
            "education": [
                {"degree": "B.Tech IT", "institution": "NIT Warangal", "start_year": 2015, "end_year": 2019}
            ],
            "redrob_signals": {
                "github_activity_score": 65.0,
                "notice_period_days": 30,
                "recruiter_response_rate": 0.75,
                "interview_completion_rate": 0.80,
                "open_to_work_flag": True,
                "saved_by_recruiters_30d": 12,
                "search_appearance_30d": 180,
                "profile_completeness_score": 88.0,
                "last_active_date": "2026-05-10",
                "verified_email": True,
                "verified_phone": True,
                "linkedin_connected": True
            }
        },
        {
            "candidate_id": "CAND_0001007",
            "profile": {
                "current_title": "Data Scientist",
                "current_company": "Meesho",
                "current_industry": "E-Commerce",
                "years_of_experience": 4.5,
                "headline": "Data Scientist - NLP & Catalog Search",
                "summary": "Developing semantic product search models and cross-lingual embeddings for vernacular buyers in India."
            },
            "career_history": [
                {
                    "title": "Data Scientist",
                    "company": "Meesho",
                    "duration_months": 30,
                    "description": "Built bi-encoder product retrieval model using HuggingFace transformers and FAISS. Evaluated offline hit rate and MRR."
                },
                {
                    "title": "Associate Data Scientist",
                    "company": "Mu Sigma",
                    "duration_months": 24,
                    "description": "Customer analytics and clustering models."
                }
            ],
            "skills": [
                {"name": "semantic search", "proficiency": "advanced", "duration_months": 24},
                {"name": "embeddings", "proficiency": "advanced", "duration_months": 26},
                {"name": "retrieval", "proficiency": "advanced", "duration_months": 22},
                {"name": "faiss", "proficiency": "intermediate", "duration_months": 18},
                {"name": "nlp", "proficiency": "expert", "duration_months": 36},
                {"name": "pytorch", "proficiency": "advanced", "duration_months": 36}
            ],
            "education": [
                {"degree": "M.Sc Statistics", "institution": "ISI Kolkata", "start_year": 2017, "end_year": 2019}
            ],
            "redrob_signals": {
                "github_activity_score": 72.0,
                "notice_period_days": 45,
                "recruiter_response_rate": 0.80,
                "interview_completion_rate": 0.82,
                "open_to_work_flag": True,
                "saved_by_recruiters_30d": 14,
                "search_appearance_30d": 195,
                "profile_completeness_score": 86.0,
                "last_active_date": "2026-05-20",
                "verified_email": True,
                "verified_phone": True,
                "linkedin_connected": True
            }
        },

        # --- Consulting Only Candidates (Penalized for consulting-only) ---
        {
            "candidate_id": "CAND_0001008",
            "profile": {
                "current_title": "Lead Consultant",
                "current_company": "TCS",
                "current_industry": "IT Services",
                "years_of_experience": 8.0,
                "headline": "Lead Consultant - Enterprise Cloud and Search Integration",
                "summary": "8 years consulting enterprise clients on legacy database migrations and Elasticsearch maintenance."
            },
            "career_history": [
                {
                    "title": "Lead Consultant",
                    "company": "TCS",
                    "duration_months": 48,
                    "description": "Client management, offshore coordination, and vendor database maintenance for banking client."
                },
                {
                    "title": "Software Consultant",
                    "company": "Infosys",
                    "duration_months": 48,
                    "description": "Java backend development and SQL optimization for insurance project."
                }
            ],
            "skills": [
                {"name": "java", "proficiency": "expert", "duration_months": 72},
                {"name": "sql", "proficiency": "expert", "duration_months": 72},
                {"name": "elasticsearch", "proficiency": "intermediate", "duration_months": 24},
                {"name": "python", "proficiency": "intermediate", "duration_months": 24}
            ],
            "education": [
                {"degree": "B.Tech IT", "institution": "Vellore Institute of Technology", "start_year": 2012, "end_year": 2016}
            ],
            "redrob_signals": {
                "github_activity_score": 10.0,
                "notice_period_days": 90,
                "recruiter_response_rate": 0.60,
                "interview_completion_rate": 0.70,
                "open_to_work_flag": False,
                "saved_by_recruiters_30d": 4,
                "search_appearance_30d": 65,
                "profile_completeness_score": 75.0,
                "last_active_date": "2026-02-15",
                "verified_email": True,
                "verified_phone": False,
                "linkedin_connected": False
            }
        },
        {
            "candidate_id": "CAND_0001009",
            "profile": {
                "current_title": "Senior Technical Analyst",
                "current_company": "Wipro",
                "current_industry": "Consulting",
                "years_of_experience": 7.0,
                "headline": "Consultant - IT Services and Enterprise Data Support",
                "summary": "7 years consulting on support projects for enterprise CRM and reporting."
            },
            "career_history": [
                {
                    "title": "Senior Technical Analyst",
                    "company": "Wipro",
                    "duration_months": 42,
                    "description": "L2/L3 application support and client ticketing."
                },
                {
                    "title": "Software Analyst",
                    "company": "Cognizant",
                    "duration_months": 42,
                    "description": "Maintenance of internal enterprise web apps."
                }
            ],
            "skills": [
                {"name": "python", "proficiency": "intermediate", "duration_months": 36},
                {"name": "sql", "proficiency": "advanced", "duration_months": 60},
                {"name": "linux", "proficiency": "advanced", "duration_months": 60}
            ],
            "education": [
                {"degree": "B.E. Computer Science", "institution": "SRM University", "start_year": 2013, "end_year": 2017}
            ],
            "redrob_signals": {
                "github_activity_score": 0.0,
                "notice_period_days": 90,
                "recruiter_response_rate": 0.45,
                "interview_completion_rate": 0.50,
                "open_to_work_flag": False,
                "saved_by_recruiters_30d": 2,
                "search_appearance_30d": 40,
                "profile_completeness_score": 68.0,
                "last_active_date": "2025-11-20",
                "verified_email": True,
                "verified_phone": False,
                "linkedin_connected": False
            }
        },

        # --- Non-Tech Role (Should be filtered or heavily penalized) ---
        {
            "candidate_id": "CAND_0001010",
            "profile": {
                "current_title": "Marketing Manager",
                "current_company": "Nykaa",
                "current_industry": "Retail",
                "years_of_experience": 6.0,
                "headline": "Digital Marketing & Brand Growth Strategist",
                "summary": "Driving paid acquisition, user retention, and creative campaigns."
            },
            "career_history": [
                {
                    "title": "Marketing Manager",
                    "company": "Nykaa",
                    "duration_months": 36,
                    "description": "Performance marketing and customer acquisition campaigns."
                }
            ],
            "skills": [
                {"name": "seo", "proficiency": "expert", "duration_months": 60},
                {"name": "google ads", "proficiency": "expert", "duration_months": 60},
                {"name": "content strategy", "proficiency": "expert", "duration_months": 60}
            ],
            "education": [
                {"degree": "MBA Marketing", "institution": "Symbiosis Pune", "start_year": 2016, "end_year": 2018}
            ],
            "redrob_signals": {
                "github_activity_score": 0.0,
                "notice_period_days": 60,
                "recruiter_response_rate": 0.50,
                "interview_completion_rate": 0.60,
                "open_to_work_flag": False,
                "saved_by_recruiters_30d": 3,
                "search_appearance_30d": 50,
                "profile_completeness_score": 80.0,
                "last_active_date": "2026-03-01",
                "verified_email": True,
                "verified_phone": True,
                "linkedin_connected": True
            }
        },

        # --- INTENTIONAL HONEYPOTS & FRAUDULENT PROFILES ---
        # Honeypot 1: Non-technical title with massive AI skills claim (Rule 1)
        {
            "candidate_id": "CAND_0001011",
            "profile": {
                "current_title": "HR Manager",
                "current_company": "Global Talent Corp",
                "current_industry": "Human Resources",
                "years_of_experience": 5.0,
                "headline": "HR Manager & Talent Acquisition Lead",
                "summary": "Talent leader claims deep mastery in vector search, semantic embeddings, FAISS, PyTorch, LangChain, Qdrant, RAG, and LLM fine-tuning."
            },
            "career_history": [
                {
                    "title": "HR Manager",
                    "company": "Global Talent Corp",
                    "duration_months": 40,
                    "description": "Recruiting and talent management."
                }
            ],
            "skills": [
                {"name": "retrieval", "proficiency": "expert", "duration_months": 36},
                {"name": "semantic search", "proficiency": "expert", "duration_months": 36},
                {"name": "vector search", "proficiency": "expert", "duration_months": 36},
                {"name": "embeddings", "proficiency": "expert", "duration_months": 36},
                {"name": "faiss", "proficiency": "expert", "duration_months": 36},
                {"name": "rag", "proficiency": "expert", "duration_months": 36},
                {"name": "pytorch", "proficiency": "expert", "duration_months": 36},
                {"name": "llms", "proficiency": "expert", "duration_months": 36},
                {"name": "machine learning", "proficiency": "expert", "duration_months": 36}
            ],
            "education": [
                {"degree": "MBA HR", "institution": "Amity University", "start_year": 2017, "end_year": 2019}
            ],
            "redrob_signals": {
                "github_activity_score": 0.0,
                "notice_period_days": 30,
                "recruiter_response_rate": 0.50,
                "interview_completion_rate": 0.40,
                "open_to_work_flag": True,
                "saved_by_recruiters_30d": 1,
                "search_appearance_30d": 30,
                "profile_completeness_score": 45.0,
                "last_active_date": "2026-01-10",
                "verified_email": True,
                "verified_phone": False,
                "linkedin_connected": False
            }
        },

        # Honeypot 2: 10+ AI skills claimed with <2 years total experience (Rule 2)
        {
            "candidate_id": "CAND_0001012",
            "profile": {
                "current_title": "Machine Learning Engineer",
                "current_company": "StartupX",
                "current_industry": "Software",
                "years_of_experience": 1.0,
                "headline": "Junior ML Engineer with claims of all advanced AI tech",
                "summary": "1 year out of college claiming advanced mastery in all AI frameworks."
            },
            "career_history": [
                {
                    "title": "Junior ML Intern",
                    "company": "StartupX",
                    "duration_months": 12,
                    "description": "Scripting and basic data cleaning."
                }
            ],
            "skills": [
                {"name": "retrieval", "proficiency": "expert", "duration_months": 12},
                {"name": "semantic search", "proficiency": "expert", "duration_months": 12},
                {"name": "vector search", "proficiency": "expert", "duration_months": 12},
                {"name": "embeddings", "proficiency": "expert", "duration_months": 12},
                {"name": "ranking", "proficiency": "expert", "duration_months": 12},
                {"name": "recommendation systems", "proficiency": "expert", "duration_months": 12},
                {"name": "llms", "proficiency": "expert", "duration_months": 12},
                {"name": "faiss", "proficiency": "expert", "duration_months": 12},
                {"name": "pytorch", "proficiency": "expert", "duration_months": 12}
            ],
            "education": [
                {"degree": "B.Tech CS", "institution": "Local College", "start_year": 2021, "end_year": 2025}
            ],
            "redrob_signals": {
                "github_activity_score": 5.0,
                "notice_period_days": 15,
                "recruiter_response_rate": 0.70,
                "interview_completion_rate": 0.60,
                "open_to_work_flag": True,
                "saved_by_recruiters_30d": 2,
                "search_appearance_30d": 40,
                "profile_completeness_score": 60.0,
                "last_active_date": "2026-05-01",
                "verified_email": True,
                "verified_phone": False,
                "linkedin_connected": False
            }
        },

        # Honeypot 3: Education Anomaly: start_year > end_year (Rule 7)
        {
            "candidate_id": "CAND_0001013",
            "profile": {
                "current_title": "AI Research Engineer",
                "current_company": "Observe.AI",
                "current_industry": "AI",
                "years_of_experience": 6.0,
                "headline": "AI Researcher - Semantic Retrieval & Transformers",
                "summary": "Fabricated timeline with impossible graduation dates."
            },
            "career_history": [
                {
                    "title": "AI Research Engineer",
                    "company": "Observe.AI",
                    "duration_months": 40,
                    "description": "Retrieval and search algorithm design."
                }
            ],
            "skills": [
                {"name": "retrieval", "proficiency": "advanced", "duration_months": 36},
                {"name": "embeddings", "proficiency": "advanced", "duration_months": 36},
                {"name": "semantic search", "proficiency": "advanced", "duration_months": 36}
            ],
            "education": [
                {"degree": "M.Tech AI", "institution": "Top Tech Institute", "start_year": 2024, "end_year": 2020} # Anomaly: start 2024 > end 2020
            ],
            "redrob_signals": {
                "github_activity_score": 40.0,
                "notice_period_days": 30,
                "recruiter_response_rate": 0.80,
                "interview_completion_rate": 0.80,
                "open_to_work_flag": True,
                "saved_by_recruiters_30d": 8,
                "search_appearance_30d": 120,
                "profile_completeness_score": 70.0,
                "last_active_date": "2026-04-10",
                "verified_email": False,
                "verified_phone": False,
                "linkedin_connected": False
            }
        },

        # Honeypot 4: Claimed 10+ years at startup founded in 2023 (Rule 8: Krutrim founded in 2023)
        {
            "candidate_id": "CAND_0001014",
            "profile": {
                "current_title": "Principal Machine Learning Engineer",
                "current_company": "Krutrim",
                "current_industry": "AI",
                "years_of_experience": 10.0,
                "headline": "Principal AI Architect at Krutrim since 2016",
                "summary": "Claims to have worked 96 months at Krutrim, which was only founded in 2023."
            },
            "career_history": [
                {
                    "title": "Principal ML Engineer",
                    "company": "Krutrim",
                    "duration_months": 96, # Anomaly: Krutrim founded in 2023!
                    "description": "Architecting large scale foundation models and retrieval platforms."
                }
            ],
            "skills": [
                {"name": "retrieval", "proficiency": "expert", "duration_months": 72},
                {"name": "semantic search", "proficiency": "expert", "duration_months": 72},
                {"name": "ranking", "proficiency": "expert", "duration_months": 72}
            ],
            "education": [
                {"degree": "B.Tech CS", "institution": "IIT Roorkee", "start_year": 2010, "end_year": 2014}
            ],
            "redrob_signals": {
                "github_activity_score": 25.0,
                "notice_period_days": 30,
                "recruiter_response_rate": 0.70,
                "interview_completion_rate": 0.70,
                "open_to_work_flag": True,
                "saved_by_recruiters_30d": 10,
                "search_appearance_30d": 140,
                "profile_completeness_score": 65.0,
                "last_active_date": "2026-03-20",
                "verified_email": True,
                "verified_phone": False,
                "linkedin_connected": False
            }
        },

        # Honeypot 5: Fake superstar profile (Rule 10: 10+ AI skills, 0 GitHub, completeness < 50)
        {
            "candidate_id": "CAND_0001015",
            "profile": {
                "current_title": "AI Engineer",
                "current_company": "Stealth AI",
                "current_industry": "AI",
                "years_of_experience": 4.0,
                "headline": "AI Wizard with zero online footprint or completeness",
                "summary": "Massive keyword list with zero verified credentials."
            },
            "career_history": [
                {
                    "title": "AI Engineer",
                    "company": "Stealth AI",
                    "duration_months": 36,
                    "description": "Deep learning and vector search."
                }
            ],
            "skills": [
                {"name": "retrieval", "proficiency": "expert", "duration_months": 30},
                {"name": "semantic search", "proficiency": "expert", "duration_months": 30},
                {"name": "vector search", "proficiency": "expert", "duration_months": 30},
                {"name": "embeddings", "proficiency": "expert", "duration_months": 30},
                {"name": "faiss", "proficiency": "expert", "duration_months": 30},
                {"name": "qdrant", "proficiency": "expert", "duration_months": 30},
                {"name": "pinecone", "proficiency": "expert", "duration_months": 30},
                {"name": "llms", "proficiency": "expert", "duration_months": 30},
                {"name": "rag", "proficiency": "expert", "duration_months": 30},
                {"name": "pytorch", "proficiency": "expert", "duration_months": 30},
                {"name": "ranking", "proficiency": "expert", "duration_months": 30}
            ],
            "education": [],
            "redrob_signals": {
                "github_activity_score": 0.0,
                "notice_period_days": 15,
                "recruiter_response_rate": 0.30,
                "interview_completion_rate": 0.20,
                "open_to_work_flag": True,
                "saved_by_recruiters_30d": 1,
                "search_appearance_30d": 15,
                "profile_completeness_score": 35.0, # Anomaly: < 50
                "last_active_date": "2025-10-01",
                "verified_email": False,
                "verified_phone": False,
                "linkedin_connected": False
            }
        }
    ]

    # Generate additional realistic variations up to 50 candidates
    companies = ["Flipkart", "Uber", "Amazon", "Observe.AI", "Yellow.ai", "PhonePe", "CRED", "Freshworks", "Infosys", "Wipro"]
    titles = [
        "Senior ML Engineer", "Search Relevance Engineer", "Recommendation Systems Engineer",
        "Applied Scientist", "NLP Engineer", "Data Scientist", "Backend Engineer", "Platform Engineer"
    ]
    
    for i in range(16, 51):
        cid = f"CAND_000{1000 + i}"
        company = companies[i % len(companies)]
        title = titles[i % len(titles)]
        is_consulting = company in ["Infosys", "Wipro", "TCS"]
        exp = round(3.0 + (i % 9) * 0.8, 1)
        
        has_retrieval = (i % 3 != 0)
        skills = [
            {"name": "python", "proficiency": "expert", "duration_months": int(exp * 10)},
            {"name": "machine learning", "proficiency": "advanced", "duration_months": int(exp * 8)},
        ]
        if has_retrieval:
            skills.extend([
                {"name": "retrieval", "proficiency": "advanced", "duration_months": int(exp * 6)},
                {"name": "embeddings", "proficiency": "advanced", "duration_months": int(exp * 5)},
                {"name": "semantic search", "proficiency": "intermediate", "duration_months": int(exp * 4)},
                {"name": "ranking", "proficiency": "advanced", "duration_months": int(exp * 5)}
            ])
        if i % 4 == 0:
            skills.append({"name": "ndcg", "proficiency": "intermediate", "duration_months": 24})
            skills.append({"name": "ab testing", "proficiency": "advanced", "duration_months": 30})

        candidate = {
            "candidate_id": cid,
            "profile": {
                "current_title": title,
                "current_company": company,
                "current_industry": "Technology",
                "years_of_experience": exp,
                "headline": f"{title} at {company} | Applied AI & Distributed Systems",
                "summary": f"{exp} years of industry experience working on machine learning pipelines, production serving, and data systems at {company}."
            },
            "career_history": [
                {
                    "title": title,
                    "company": company,
                    "duration_months": int(exp * 12 * 0.6),
                    "description": f"Developed machine learning models and engineering workflows at scale for {company}."
                }
            ],
            "skills": skills,
            "education": [
                {"degree": "B.Tech Computer Science", "institution": "Reputed University", "start_year": int(2026 - exp - 4), "end_year": int(2026 - exp)}
            ],
            "redrob_signals": {
                "github_activity_score": round(max(5.0, (i * 7) % 95), 1),
                "notice_period_days": [15, 30, 45, 60, 90][i % 5],
                "recruiter_response_rate": round(0.55 + ((i * 3) % 40) / 100, 2),
                "interview_completion_rate": round(0.60 + ((i * 2) % 35) / 100, 2),
                "open_to_work_flag": (i % 2 == 0),
                "saved_by_recruiters_30d": (i * 3) % 25,
                "search_appearance_30d": 50 + (i * 12) % 250,
                "profile_completeness_score": round(70.0 + (i * 2) % 28, 1),
                "last_active_date": f"2026-05-{10 + (i % 20):02d}",
                "verified_email": True,
                "verified_phone": (i % 3 != 0),
                "linkedin_connected": (i % 2 == 0)
            }
        }
        candidates.append(candidate)

    return candidates
