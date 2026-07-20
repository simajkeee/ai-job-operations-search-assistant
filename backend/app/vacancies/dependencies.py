from typing import Annotated

from fastapi import Depends
from openai import OpenAI
from sqlalchemy.orm import Session

from app.infrastructure.database import get_db_session
from app.job_preferences.persistence import SqlAlchemyJobPreferenceRepository
from app.vacancies.analyze import AnalyzeVacancy
from app.vacancies.analyzer import VacancyAnalyzer, OpenAIVacancyAnalyzer
from app.infrastructure.settings import Settings, get_settings


def get_vacancy_analyzer(
    settings: Annotated[Settings, Depends(get_settings)],
) -> VacancyAnalyzer:
    if settings.openai_api_key is None:
        raise RuntimeError("OPENAI_API_KEY is not configured")

    return OpenAIVacancyAnalyzer(
        OpenAI(api_key=settings.openai_api_key.get_secret_value()),
    )


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
