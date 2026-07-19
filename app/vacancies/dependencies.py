import os
from typing import Annotated

from fastapi import Depends
from openai import OpenAI
from sqlalchemy.orm import Session

from app.infrastructure.database import get_db_session
from app.job_preferences.persistence import SqlAlchemyJobPreferenceRepository
from app.vacancies.analyze import AnalyzeVacancy
from app.vacancies.analyzer import VacancyAnalyzer, OpenAIVacancyAnalyzer


def get_vacancy_analyzer() -> VacancyAnalyzer:
    return OpenAIVacancyAnalyzer(OpenAI(api_key=os.getenv("OPENAI_API_KEY")))


def get_analyze_vacancy(
    session: Annotated[Session, Depends(get_db_session)],
    vacancy_analyzer: Annotated[
        VacancyAnalyzer,
        Depends(get_vacancy_analyzer),
    ],
) -> AnalyzeVacancy:
    return AnalyzeVacancy(
        job_preferences=SqlAlchemyJobPreferenceRepository(session),
        vacancy_analyzer=vacancy_analyzer,
    )
