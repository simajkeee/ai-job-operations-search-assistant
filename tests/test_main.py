from typing import Generator

import pytest
from fastapi.testclient import TestClient

from main import app, get_vacancy_analyzer
from tests.fakes import FakeVacancyAnalyzer


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_vacancy_analyzer] = lambda: FakeVacancyAnalyzer()

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_vacancy_analyzer, None)


@pytest.mark.parametrize(
    ("vacancy_text", "decision"),
    [
        ("Python FastAPI developer", "apply"),
        ("Python developer", "apply_with_caveats"),
        ("PHP Symfony developer", "skip"),
    ],
)
def test_analyze_vacancy_returns_expected_decision(
    client: TestClient,
    vacancy_text: str,
    decision: str,
) -> None:
    response = client.post(
        "/api/v1/vacancies/analyze",
        json={"vacancy_text": vacancy_text},
    )

    assert response.status_code == 200
    assert response.json()["decision"] == decision
