from uuid import UUID

from app.job_preferences.domain import JobPreference
from app.job_preferences.unit_of_work import JobPreferenceUnitOfWork


class ReplaceJobPreferences:
    def __init__(self, unit_of_work: JobPreferenceUnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    def execute(
        self, user_id: UUID, preferences: list[JobPreference]
    ) -> list[JobPreference]:
        try:
            user_job_preferences = self._unit_of_work.job_preferences.replace_for_user(
                user_id, preferences
            )
            self._unit_of_work.commit()
        except Exception:
            self._unit_of_work.rollback()
            raise

        return user_job_preferences
