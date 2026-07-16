from analyzer import FakeVacancyAnalyzer
from schemas import VacancyAnalyzeRequest, Decision


def test_analyzer_decision_is_apply():
    text = "Python FastAPI developer"
    result = FakeVacancyAnalyzer().analyze(VacancyAnalyzeRequest(vacancy_text=text))

    assert result.decision == Decision.APPLY


def test_analyzer_decision_is_apply_with_caveats():
    text = "Python developer"
    result = FakeVacancyAnalyzer().analyze(VacancyAnalyzeRequest(vacancy_text=text))

    assert result.decision == Decision.APPLY_WITH_CAVEATS


def test_analyzer_decision_is_skip():
    text = "PHP Symfony developer"
    result = FakeVacancyAnalyzer().analyze(VacancyAnalyzeRequest(vacancy_text=text))

    assert result.decision == Decision.SKIP
