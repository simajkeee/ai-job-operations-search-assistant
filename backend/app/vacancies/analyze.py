from uuid import UUID

from app.job_preferences.domain import JobPreference
from app.job_preferences.repository import JobPreferenceRepository
from app.vacancies.analyzer import VacancyAnalyzer
from app.vacancies.errors import NoJobPreferencesError, InvalidVacancyAnalysisError
from app.vacancies.schemas import VacancyAnalyzeResponse, Decision


class AnalyzeVacancy:
    def __init__(
        self,
        job_preferences: JobPreferenceRepository,
        vacancy_analyzer: VacancyAnalyzer,
    ):
        self._job_preferences = job_preferences
        self._vacancy_analyzer = vacancy_analyzer

    def execute(
        self, user_id: UUID, vacancy_title: str, vacancy_text: str
    ) -> VacancyAnalyzeResponse:
        preferences = self._job_preferences.list_for_user(user_id)

        if not preferences:
            raise NoJobPreferencesError()

        analysis = self._vacancy_analyzer.analyze(
            vacancy_title=vacancy_title,
            vacancy_text=vacancy_text,
            job_preferences=preferences,
        )

        self._validate_analysis(analysis, preferences)

        return analysis

    def _validate_analysis(
        self, analysis: VacancyAnalyzeResponse, preferences: list[JobPreference]
    ) -> None:
        preference = next(
            (
                item
                for item in preferences
                if item.id == analysis.matched_job_preference_id
            ),
            None,
        )

        if analysis.decision is Decision.SKIP:
            if analysis.recommended_resume is not None:
                raise InvalidVacancyAnalysisError()

            if analysis.matched_job_preference_id is not None and preference is None:
                raise InvalidVacancyAnalysisError()

            return

        if preference is None:
            raise InvalidVacancyAnalysisError()

        if analysis.recommended_resume != preference.resume_label:
            raise InvalidVacancyAnalysisError()
