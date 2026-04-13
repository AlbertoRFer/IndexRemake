from collections.abc import Generator

import pytest
import sqlalchemy as sa
from sqlalchemy import orm

from indexremake.infrastructure.persistence.database import mappings, tables


@pytest.fixture
def db_engine() -> sa.Engine:
    engine = sa.create_engine("sqlite:///:memory:")
    tables.metadata.create_all(engine)
    return engine


@pytest.fixture
def db_session(db_engine: sa.Engine) -> Generator[orm.Session]:
    mappings.start_mappers()
    yield orm.sessionmaker(bind=db_engine)()
    orm.clear_mappers()
