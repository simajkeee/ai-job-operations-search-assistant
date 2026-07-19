from typing import Annotated

from fastapi import Depends, APIRouter

from app.auth.dependencies import get_current_user
from app.auth.domain import User
from app.job_preferences.dependencies import (
    get_job_preference_repository,
    get_replace_job_preferences,
)
from app.job_preferences.replace import ReplaceJobPreferences
from app.job_preferences.repository import JobPreferenceRepository
from app.job_preferences.schemas import (
    JobPreferenceResponse,
    ReplaceJobPreferencesRequest,
)

router = APIRouter(prefix="/job-preferences", tags=["job-preferences"])


@router.get("", response_model=list[JobPreferenceResponse])
def list_job_preferences(
    current_user: Annotated[User, Depends(get_current_user)],
    repository: Annotated[
        JobPreferenceRepository, Depends(get_job_preference_repository)
    ],
) -> list[JobPreferenceResponse]:
    job_preferences = repository.list_for_user(current_user.id)

    return list(map(JobPreferenceResponse.from_domain, job_preferences))


@router.put("", response_model=list[JobPreferenceResponse])
def replace_job_preferences(
    request: ReplaceJobPreferencesRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    replace_job_preferences_service: Annotated[
        ReplaceJobPreferences, Depends(get_replace_job_preferences)
    ],
) -> list[JobPreferenceResponse]:
    user_preferences = [
        preference.to_domain(current_user.id) for preference in request.preferences
    ]

    updated_user_preferences = replace_job_preferences_service.execute(
        current_user.id, user_preferences
    )

    return list(map(JobPreferenceResponse.from_domain, updated_user_preferences))
