from uuid import UUID

from pydantic import BaseModel
from enum import Enum

from app.job_preferences.domain import WorkMode


class VacancyAnalyzeRequest(BaseModel):
    vacancy_title: str
    vacancy_text: str


class Decision(Enum):
    APPLY = "apply"
    APPLY_WITH_CAVEATS = "apply_with_caveats"
    SKIP = "skip"


class RoleMatch(str, Enum):
    STRONG = "strong"
    PARTIAL = "partial"
    NONE = "none"


class VacancyAnalyzeResponse(BaseModel):
    decision: Decision
    recommended_resume: str | None
    matched_job_preference_id: UUID | None
    interpreted_role: str | None
    role_match: RoleMatch
    role_evidence: list[str]
    matched_keywords: list[str]
    unmatched_preference_keywords: list[str]
    detected_work_modes: list[WorkMode]
    work_mode_match: bool | None
    critical_gaps: list[str]
    reasoning: str
