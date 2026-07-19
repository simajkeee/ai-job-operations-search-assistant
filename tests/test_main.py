from datetime import datetime, timezone
from typing import Generator
from unittest.mock import Mock
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.auth.dependencies import get_current_user
from app.auth.domain import User
from app.vacancies.analyze import AnalyzeVacancy
from app.vacancies.dependencies import get_analyze_vacancy
from app.vacancies.schemas import VacancyAnalyzeResponse, Decision, RoleMatch
from main import app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    authenticated_user = User(
        id=uuid4(),
        email="test@example.com",
        password_hash="not-user",
        created_at=datetime.now(timezone.utc),
    )

    analyze_vacancy = Mock(spec=AnalyzeVacancy)
    analyze_vacancy.execute.return_value = VacancyAnalyzeResponse(
        decision=Decision.SKIP,
        recommended_resume=None,
        matched_job_preference_id=None,
        interpreted_role=None,
        role_match=RoleMatch.NONE,
        role_evidence=[],
        matched_keywords=[],
        unmatched_preference_keywords=[],
        detected_work_modes=[],
        work_mode_match=None,
        critical_gaps=[],
        reasoning="Fake analysis result.",
    )
    app.dependency_overrides[get_analyze_vacancy] = lambda: analyze_vacancy
    app.dependency_overrides[get_current_user] = lambda: authenticated_user

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_analyze_vacancy, None)
        app.dependency_overrides.pop(get_current_user, None)


@pytest.mark.parametrize(
    ("vacancy_title", "vacancy_text", "decision"),
    [
        ("Backend developer FastAPI", "Python FastAPI developer", "skip"),
    ],
)
def test_analyze_vacancy_returns_expected_decision(
    client: TestClient,
    vacancy_title: str,
    vacancy_text: str,
    decision: str,
) -> None:
    response = client.post(
        "/api/v1/vacancies/analyze",
        json={"vacancy_title": vacancy_title, "vacancy_text": vacancy_text},
    )

    assert response.status_code == 200
    assert response.json()["decision"] == decision
