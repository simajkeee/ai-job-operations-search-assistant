from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, String, DateTime, func, select
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column, Session

from app.infrastructure.database import Base
from app.job_preferences.domain import JobPreference, WorkMode
from app.job_preferences.repository import JobPreferenceRepository


class JobPreferenceModel(Base):
    __tablename__ = "job_preferences"

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    user_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    target_title: Mapped[str] = mapped_column(String(255), nullable=False)
    keywords: Mapped[list[str]] = mapped_column(JSONB, nullable=False)
    accepted_work_modes: Mapped[list[str]] = mapped_column(JSONB, nullable=False)
    resume_label: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        onupdate=func.now(),
    )


class SqlAlchemyJobPreferenceRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def list_for_user(self, user_id: UUID) -> list[JobPreference]:
        statement = select(JobPreferenceModel).where(
            JobPreferenceModel.user_id == user_id
        )
        users_job_preferences = self._session.scalars(statement).all()

        return list(map(self._to_domain_model, users_job_preferences))

    def replace_for_user(
        self, user_id: UUID, preferences: list[JobPreference]
    ) -> list[JobPreference]:
        self._session.query(JobPreferenceModel).filter(
            JobPreferenceModel.user_id == user_id
        ).delete()

        updated_models = []
        for preference in preferences:
            model = JobPreferenceModel(
                user_id=user_id,
                target_title=preference.target_title,
                keywords=preference.keywords,
                accepted_work_modes=[
                    mode.value for mode in preference.accepted_work_modes
                ],
                resume_label=preference.resume_label,
            )

            if preference.id is not None:
                model.id = preference.id

            updated_models.append(model)

        self._session.add_all(updated_models)
        self._session.flush()

        return list(map(self._to_domain_model, updated_models))

    @staticmethod
    def _to_domain_model(job_preference: JobPreferenceModel) -> JobPreference:
        return JobPreference(
            id=job_preference.id,
            user_id=job_preference.user_id,
            target_title=job_preference.target_title,
            keywords=job_preference.keywords,
            accepted_work_modes=[
                WorkMode(mode) for mode in job_preference.accepted_work_modes
            ],
            resume_label=job_preference.resume_label,
        )


class SqlAlchemyJobPreferenceUnitOfWork:
    def __init__(self, session: Session) -> None:
        self._session = session
        self._job_preferences = SqlAlchemyJobPreferenceRepository(self._session)

    @property
    def job_preferences(self) -> JobPreferenceRepository:
        return self._job_preferences

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()
