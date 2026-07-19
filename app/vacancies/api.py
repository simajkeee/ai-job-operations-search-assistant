from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends

from app.auth.dependencies import get_current_user
from app.auth.domain import User
from app.vacancies.analyze import AnalyzeVacancy
from app.vacancies.dependencies import get_analyze_vacancy
from app.vacancies.errors import NoJobPreferencesError, InvalidVacancyAnalysisError
from app.vacancies.schemas import VacancyAnalyzeRequest, VacancyAnalyzeResponse

router = APIRouter(prefix="/vacancies", tags=["vacancies"])


@router.post("/analyze", response_model=VacancyAnalyzeResponse)
def analyze_vacancy(
    vacancy_analyze_request: VacancyAnalyzeRequest,
    analyze_vacancy_service: Annotated[AnalyzeVacancy, Depends(get_analyze_vacancy)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> VacancyAnalyzeResponse:
    try:
        return analyze_vacancy_service.execute(
            current_user.id,
            vacancy_analyze_request.vacancy_title,
            vacancy_analyze_request.vacancy_text,
        )
    except NoJobPreferencesError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Create at least one job preference before analyzing vacancies",
        ) from error
    except InvalidVacancyAnalysisError as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Analysis provider returned an invalid result",
        ) from error
