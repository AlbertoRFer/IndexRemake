from collections.abc import Generator

import pytest
from sqlalchemy import orm

from indexremake.infrastructure.persistence import database


@pytest.fixture
def test_db() -> Generator[database.SQLiteDatabase]:
    db = database.SQLiteDatabase(":memory:")
    yield db
    db.dispose()


@pytest.fixture
def db_session(test_db: database.SQLiteDatabase) -> Generator[orm.Session]:
    session = test_db.get_session()
    yield session
    session.close()
