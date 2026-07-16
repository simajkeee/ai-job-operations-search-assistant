import os
from typing import Annotated

from fastapi import FastAPI, Depends
from openai import OpenAI

from analyzer import VacancyAnalyzer, OpenAIVacancyAnalyzer
from schemas import VacancyAnalyzeRequest, VacancyAnalyzeResponse

app = FastAPI()


def get_vacancy_analyzer() -> VacancyAnalyzer:
    return OpenAIVacancyAnalyzer(OpenAI(api_key=os.getenv("OPENAI_API_KEY")))


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/v1/vacancies/analyze", response_model=VacancyAnalyzeResponse)
def analyze_vacancy(
    vacancy_analyze_request: VacancyAnalyzeRequest,
    vacancy_analyzer: Annotated[VacancyAnalyzer, Depends(get_vacancy_analyzer)],
) -> VacancyAnalyzeResponse:
    return vacancy_analyzer.analyze(vacancy_analyze_request)
