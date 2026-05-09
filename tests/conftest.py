from collections.abc import Generator

import pytest

from indexremake.infrastructure.persistence import database
from tests.support import factories


@pytest.fixture
def seed_data() -> list[factories.FolderData]:
    return []  # Overwrite in test files if seeded db is needed


@pytest.fixture
def db(seed_data: list[factories.FolderData]) -> Generator[database.SQLiteDatabase]:
    db = database.SQLiteDatabase(":memory:")

    yield db
    db.dispose()


@pytest.fixture
def seeded_db(
    db: database.SQLiteDatabase, seed_data: list[factories.FolderData]
) -> database.SQLiteDatabase:
    factories.insert_folder_data_into_db(db.get_session(), seed_data)
    return db
