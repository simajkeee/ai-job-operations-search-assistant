from typing import Protocol

from app.job_preferences.repository import JobPreferenceRepository


class JobPreferenceUnitOfWork(Protocol):
    @property
    def job_preferences(self) -> JobPreferenceRepository: ...

    def commit(self) -> None: ...

    def rollback(self) -> None: ...
