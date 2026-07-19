from schemas import VacancyAnalyzeRequest, VacancyAnalyzeResponse, Decision, RoleMatch


class FakeVacancyAnalyzer:
    def analyze(
        self, vacancy_analyze_request: VacancyAnalyzeRequest
    ) -> VacancyAnalyzeResponse:
        return VacancyAnalyzeResponse(
            decision=Decision.SKIP,
            recommended_resume=None,
            matched_job_preference_id=None,
            interpreted_role=None,
            role_match=RoleMatch.NONE,
            role_evidence=[],
            matched_keywords=[],
            unmatched_preference_keywords=[],
            detected_work_modes=[],
            work_mode_match=None,
            critical_gaps=[],
            reasoning="Fake analysis result.",
        )
