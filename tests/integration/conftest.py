from collections.abc import Generator

import pytest
import sqlalchemy as sa
from sqlalchemy import orm

from indexremake.infrastructure.persistence import database


@pytest.fixture(scope="session", autouse=True)
def setup_mappers() -> None:
    database.start_mappers()


@pytest.fixture
def test_db() -> database.Database:
    db = database.Database(":memory:")
    db.create_all()
    return db


@pytest.fixture
def db_session(test_db: database.Database) -> Generator[orm.Session]:
    session = test_db.get_session()
    yield session
    session.rollback()
