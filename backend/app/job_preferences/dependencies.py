from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.infrastructure.database import get_db_session
from app.job_preferences.persistence import (
    SqlAlchemyJobPreferenceUnitOfWork,
    SqlAlchemyJobPreferenceRepository,
)
from app.job_preferences.replace import ReplaceJobPreferences
from app.job_preferences.repository import JobPreferenceRepository


def get_replace_job_preferences(
    session: Annotated[Session, Depends(get_db_session)],
) -> ReplaceJobPreferences:
    return ReplaceJobPreferences(
        unit_of_work=SqlAlchemyJobPreferenceUnitOfWork(session),
    )


def get_job_preference_repository(
    session: Annotated[Session, Depends(get_db_session)],
) -> JobPreferenceRepository:
    return SqlAlchemyJobPreferenceRepository(session)
