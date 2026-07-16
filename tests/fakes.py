from schemas import VacancyAnalyzeRequest, VacancyAnalyzeResponse, Decision


class FakeVacancyAnalyzer:
    def analyze(
        self, vacancy_analyze_request: VacancyAnalyzeRequest
    ) -> VacancyAnalyzeResponse:
        skills = ["python", "fastapi"]
        found_skills = [
            s for s in skills if s in vacancy_analyze_request.vacancy_text.lower()
        ]
        decision = Decision.SKIP
        if len(found_skills) == 2:
            decision = Decision.APPLY
        elif len(found_skills) == 1 and found_skills[0] == "python":
            decision = Decision.APPLY_WITH_CAVEATS

        return VacancyAnalyzeResponse(
            decision=decision,
            recommended_resume="python_backend",
            matched_requirements=found_skills,
            critical_gaps=[],
            reasoning="The vacancy requires a Python backend developer with experience in building scalable web applications.",
        )
