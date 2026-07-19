from fastapi import FastAPI, APIRouter

from app.auth.api import router as auth_router
from app.job_preferences.api import router as job_preferences_router
from app.vacancies.api import router as vacancies_router

app = FastAPI()

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(auth_router)
api_v1_router.include_router(job_preferences_router)
api_v1_router.include_router(vacancies_router)

app.include_router(api_v1_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
