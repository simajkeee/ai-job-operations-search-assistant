import os
from typing import Annotated

from fastapi import FastAPI, Depends
from openai import OpenAI

from analyzer import VacancyAnalyzer, OpenAIVacancyAnalyzer
from app.auth.dependencies import get_current_user
from app.auth.domain import User
from schemas import VacancyAnalyzeRequest, VacancyAnalyzeResponse

from app.auth.api import router as auth_router

app = FastAPI()
app.include_router(auth_router)


def get_vacancy_analyzer() -> VacancyAnalyzer:
    return OpenAIVacancyAnalyzer(OpenAI(api_key=os.getenv("OPENAI_API_KEY")))


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/v1/vacancies/analyze", response_model=VacancyAnalyzeResponse)
def analyze_vacancy(
    vacancy_analyze_request: VacancyAnalyzeRequest,
    vacancy_analyzer: Annotated[VacancyAnalyzer, Depends(get_vacancy_analyzer)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> VacancyAnalyzeResponse:
    return vacancy_analyzer.analyze(vacancy_analyze_request)
