from dataclasses import dataclass
from enum import Enum
from uuid import UUID


class WorkMode(str, Enum):
    REMOTE = "remote"
    HYBRID = "hybrid"
    OFFICE = "office"


@dataclass
class JobPreference:
    id: UUID | None
    user_id: UUID
    target_title: str
    keywords: list[str]
    accepted_work_modes: list[WorkMode]
    resume_label: str | None
