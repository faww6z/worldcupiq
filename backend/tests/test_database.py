from sqlalchemy import text
from sqlalchemy.orm import Session


def test_database_connection(db_session: Session) -> None:
    assert db_session.execute(text("select 1")).scalar_one() == 1

