from datetime import datetime, timezone
from typing import Generator
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.auth.dependencies import get_current_user
from app.auth.domain import User
from main import app, get_vacancy_analyzer
from tests.fakes import FakeVacancyAnalyzer


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    authenticated_user = User(
        id=uuid4(),
        email="test@example.com",
        password_hash="not-user",
        created_at=datetime.now(timezone.utc),
    )

    app.dependency_overrides[get_vacancy_analyzer] = lambda: FakeVacancyAnalyzer()
    app.dependency_overrides[get_current_user] = lambda: authenticated_user

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_vacancy_analyzer, None)
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
