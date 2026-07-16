from typing import Protocol
from openai import OpenAI

from schemas import Decision, VacancyAnalyzeRequest, VacancyAnalyzeResponse


class VacancyAnalyzer(Protocol):
    def analyze(
        self, vacancy_analyze_request: VacancyAnalyzeRequest
    ) -> VacancyAnalyzeResponse: ...


class OpenAIVacancyAnalyzer:
    def __init__(self, open_ai_client: OpenAI):
        self.open_ai_client = open_ai_client

    def analyze(
        self, vacancy_analyze_request: VacancyAnalyzeRequest
    ) -> VacancyAnalyzeResponse:
        response = self.open_ai_client.responses.parse(
            model="gpt-5.6-luna",
            instructions="""
                You are a job-application analyst.
                
                Candidate profile:
                - Target role: Python backend developer.
                - Strong skills: Python and FastAPI.
                - Available resume: python_backend.
                
                Analyze the vacancy text against this candidate profile.
                
                Choose exactly one decision:
                - apply: Python and FastAPI are clear core requirements, with no critical mismatch.
                - apply_with_caveats: the input is a recognizable vacancy for a Python backend role, but FastAPI is missing, unclear, or there are non-critical gaps.
                - skip: the input is not a recognizable job vacancy; it lacks a role, responsibilities, or requirements; Python is not a core requirement; or there is a critical mismatch.
                
                Return:
                - decision: one of apply, apply_with_caveats, skip.
                - recommended_resume: python_backend when applying or applying with caveats; null when skipping.
                - matched_requirements: only requirements explicitly present in the vacancy and matched by the candidate.
                - critical_gaps: only meaningful missing or incompatible requirements. Use an empty list if none.
                - reasoning: a concise explanation grounded only in the vacancy text and candidate profile.
                
                If the input is not a meaningful job-vacancy description, return skip.
                Use apply_with_caveats only when it is clearly a vacancy that is plausibly relevant to the candidate but lacks some non-critical information.            """,
            input=vacancy_analyze_request.vacancy_text,
            text_format=VacancyAnalyzeResponse,
        )

        analysis = response.output_parsed
        if analysis is None:
            raise RuntimeError("OpenAI returned no structured analysis")

        return analysis


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
