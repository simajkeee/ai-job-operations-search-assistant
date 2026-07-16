import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.mark.parametrize(
    ("vacancy_text", "decision"),
    [
        ("Python FastAPI developer", "apply"),
        ("Python developer", "apply_with_caveats"),
        ("PHP Symfony developer", "skip"),
    ],
)
def test_analyze_vacancy_returns_expected_decision(
    vacancy_text: str, decision: str
) -> None:
    response = client.post(
        "/api/v1/vacancies/analyze",
        json={"vacancy_text": vacancy_text},
    )

    assert response.status_code == 200
    assert response.json()["decision"] == decision
