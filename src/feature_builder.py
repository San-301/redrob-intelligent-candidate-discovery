# src/features/feature_builder.py

from typing import Dict


class FeatureBuilder:

    def build(
        self,
        candidate_features: Dict,
        jd_features: Dict
    ) -> Dict:

        years_exp = candidate_features[
            "years_experience"
        ]

        experience_score = (
            self._experience_score(
                years_exp,
                jd_features["min_exp"],
                jd_features["max_exp"]
            )
        )

        ai_score = min(
            candidate_features[
                "ai_skill_count"
            ] / 10,
            1.0
        )

    
        retrieval_score = min(
            candidate_features[
                "retrieval_skill_count"
            ] / 5,
            1.0
        )

        evaluation_score = min(
            candidate_features[
                "evaluation_skill_count"
            ] / 3,
            1.0
        )

        github_score = max(
            candidate_features[
                "github_score"
            ],
            0
        ) / 100

        engagement_score = min(
            (
                candidate_features["response_rate"] * 0.30
                +
                candidate_features["interview_completion"] * 0.25
                +
                (
                    candidate_features["profile_completeness"] / 100
                ) * 0.20
                +
                candidate_features.get(
                    "recent_activity_score",
                    0
                ) * 0.25
            ),
            1.0
        )
        
        title_score = (
            candidate_features[
                "title_strength"
            ]
        )
        
        product_company_score = min(
            candidate_features[
                "product_company_exp"
            ] / 2,
            1.0
        )

        ai_company_score = min(
            candidate_features[
                "ai_company_exp"
            ],
            1.0
        )

        ai_experience_score = min(
            candidate_features[
                "ai_months"
            ] / 60,
            1.0
        )

        career_ai_score = (
            candidate_features[
                "career_ai_score"
            ]
        )

        evaluation_experience_score = (
            1.0
            if candidate_features[
                "evaluation_experience"
            ]
            else 0.0
        )

        non_ai_title_penalty = (
            1.0
            if candidate_features[
                "non_ai_title_penalty"
            ]
            else 0.0
        )

        leadership_score = (
            candidate_features[
                "leadership_score"
            ]
        )

        open_to_work_bonus = (
            1.0
            if candidate_features[
                "open_to_work"
            ]
            else 0.0
        )

        notice_penalty = (
            self._notice_penalty(
                candidate_features[
                    "notice_period"
                ]
            )
        )

        consulting_penalty = (
            1.0
            if candidate_features[
                "consulting_only"
            ]
            else 0.0
        )

        skill_overlap_score = min(
            candidate_features.get(
                "matched_skill_count",
                0
            ) /
            max(
                jd_features.get(
                    "required_skill_count",
                    1
                ),
                1
            ),
            1.0
        )

        return {

            "candidate_id":
                candidate_features[
                    "candidate_id"
                ],

            "experience_score":
                experience_score,

            "title_score":
                title_score,

            "ai_score":
                ai_score,

            "retrieval_score":
                retrieval_score,

            "evaluation_score":
                evaluation_score,

            "github_score":
                github_score,

            "engagement_score":
                engagement_score,

            "product_company_score":
                product_company_score,

            "ai_company_score":
                ai_company_score,

            "ai_experience_score":
                ai_experience_score,
            
            "years_experience":
                years_exp,
            
            "career_ai_score":
                career_ai_score,

            "evaluation_experience_score":
                evaluation_experience_score,

            "non_ai_title_penalty":
                non_ai_title_penalty,

            "leadership_score":
                leadership_score,

            "open_to_work_bonus":
                open_to_work_bonus,

            "notice_penalty":
                notice_penalty,

            "consulting_penalty":
                consulting_penalty,
            
            "skill_overlap_score":
                skill_overlap_score,

            "saved_by_recruiters":
                candidate_features[
                    "saved_by_recruiters"
                ],

            "search_appearance":
                candidate_features[
                    "search_appearance"
                ],

            "honeypot_penalty":
                candidate_features.get(
                    "honeypot_penalty",
                    0
                ),

            "response_rate":
                candidate_features["response_rate"],

            "interview_completion":
                candidate_features["interview_completion"],

            "recent_activity_score":
            candidate_features.get(
                "recent_activity_score",
                0
            ),
            
            "production_score":
                candidate_features.get(
                    "production_score",
                    0
                ),

            "pure_research_penalty":
            candidate_features.get(
                "pure_research_penalty",
                0
            ),

            "suspicious_skill_penalty":
            min(
                candidate_features.get(
                    "suspicious_skill_count",
                    0
                ) / 5,
                1.0
            ),
            
        }

    @staticmethod
    def _experience_score(
        years,
        min_exp,
        max_exp
    ):

        if min_exp <= years <= max_exp:
            return 1.0

        if years < min_exp:
            return max(
                0,
                years / min_exp
            )

        return max(
            0,
            1 - (
                (years - max_exp) / 10
            )
        )

    @staticmethod
    def _notice_penalty(days):

        if days <= 30:
            return 0.0

        if days <= 60:
            return 0.10

        if days <= 90:
            return 0.20

        if days <= 120:
            return 0.40

        return 0.60