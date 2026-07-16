from unittest.mock import Mock

from sqlalchemy.orm import Session

from app.auth.persistence import SqlAlchemyUnitOfWork


def test_unit_of_work_commit_calls_session_commit() -> None:
    session = Mock(spec=Session)
    unit_of_work = SqlAlchemyUnitOfWork(session)

    unit_of_work.commit()

    session.commit.assert_called_once()


def test_unit_of_work_rollback_calls_session_rollback() -> None:
    session = Mock(spec=Session)
    unit_of_work = SqlAlchemyUnitOfWork(session)

    unit_of_work.rollback()

    session.rollback.assert_called_once()
