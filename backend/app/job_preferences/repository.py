from typing import Protocol
from uuid import UUID

from app.job_preferences.domain import JobPreference


class JobPreferenceRepository(Protocol):
    def list_for_user(self, user_id: UUID) -> list[JobPreference]: ...

    def replace_for_user(
        self, user_id: UUID, preferences: list[JobPreference]
    ) -> list[JobPreference]: ...
