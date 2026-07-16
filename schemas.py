from pydantic import BaseModel
from enum import Enum


class VacancyAnalyzeRequest(BaseModel):
    vacancy_text: str


class Decision(Enum):
    APPLY = "apply"
    APPLY_WITH_CAVEATS = "apply_with_caveats"
    SKIP = "skip"


class VacancyAnalyzeResponse(BaseModel):
    decision: Decision
    recommended_resume: str | None
    matched_requirements: list[str]
    critical_gaps: list[str]
    reasoning: str


class ResumeProfile(BaseModel):
    id: str
    roles: list[str]
    skills: list[str]


class CandidateProfile(BaseModel):
    preferred_roles: list[str]
    resumes: list[ResumeProfile]
