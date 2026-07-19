from typing import Self
from uuid import UUID

from pydantic import BaseModel

from app.job_preferences.domain import WorkMode, JobPreference


class JobPreferenceInput(BaseModel):
    id: UUID | None = None
    target_title: str
    keywords: list[str]
    accepted_work_modes: list[WorkMode]
    resume_label: str | None = None

    def to_domain(self, user_id: UUID) -> JobPreference:
        return JobPreference(
            id=self.id,
            user_id=user_id,
            target_title=self.target_title,
            keywords=self.keywords,
            accepted_work_modes=self.accepted_work_modes,
            resume_label=self.resume_label,
        )


class ReplaceJobPreferencesRequest(BaseModel):
    preferences: list[JobPreferenceInput]


class JobPreferenceResponse(BaseModel):
    id: UUID
    target_title: str
    keywords: list[str]
    accepted_work_modes: list[WorkMode]
    resume_label: str | None

    @classmethod
    def from_domain(cls, domain_model: JobPreference) -> Self:
        if domain_model.id is None:
            raise RuntimeError(
                "Cannot create a response from an unsaved job preference"
            )

        return cls(
            id=domain_model.id,
            target_title=domain_model.target_title,
            keywords=domain_model.keywords,
            accepted_work_modes=domain_model.accepted_work_modes,
            resume_label=domain_model.resume_label,
        )
