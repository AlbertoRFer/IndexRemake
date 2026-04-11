from collections.abc import Generator

import pytest
import sqlalchemy
from sqlalchemy import orm

from indexremake import domain
from indexremake.infrastructure.persistence import base, mappings


@pytest.fixture
def db_engine() -> sqlalchemy.Engine:
    engine = sqlalchemy.create_engine("sqlite:///:memory:")
    base.metadata.create_all(engine)
    return engine


@pytest.fixture
def db_session(db_engine: sqlalchemy.Engine) -> Generator[orm.Session]:
    mappings.start_mappers()
    yield orm.sessionmaker(bind=db_engine)()
    orm.clear_mappers()


def insert_users(db_session: orm.Session) -> None:
    db_session.execute(
        sqlalchemy.text("""
        INSERT INTO users (document_id, position, first_name, middle_name, last_name1, last_name2)
        VALUES
            (1, 1, 'John', NULL, 'Doe', 'Tre'),
            (1, 2, 'Jane', NULL, 'Doe', 'Fire'),
            (2, 1, 'Juan', 'Eriberto', 'Five', 'Six of Seven'),
            (3, 1, 'Camilo', NULL, 'Cruz', 'Pereira'),
            (3, 2, 'Amalia', 'de la Caridad', 'Rodríguez', 'Díaz'),
            (3, 3, 'Marco', 'Polo', 'Traveller', NULL)
        """)
    )


def insert_documents(db_session: orm.Session) -> None:
    db_session.execute(
        sqlalchemy.text("""
        INSERT INTO documents (folder_id, document_number, title)
        VALUES
            (1, 1, 'Document 1'),
            (1, 2, 'Document 2'),
            (2, 3, 'Document 3')
        """)
    )


def insert_folders(db_session: orm.Session) -> None:
    db_session.execute(
        sqlalchemy.text("""
        INSERT INTO folders (year)
        VALUES
            (2025),
            (2026)
        """)
    )


USERS = [
    domain.User("John", None, "Doe", "Tre"),
    domain.User("Jane", None, "Doe", "Fire"),
    domain.User("Juan", "Eriberto", "Five", "Six of Seven"),
    domain.User("Camilo", None, "Cruz", "Pereira"),
    domain.User("Amalia", "de la Caridad", "Rodríguez", "Díaz"),
    domain.User("Marco", "Polo", "Traveller", None),
]

DOCUMENTS = [
    domain.Document(1, "Document 1", [USERS[0], USERS[1]]),
    domain.Document(2, "Document 2", [USERS[2]]),
    domain.Document(3, "Document 3", [USERS[3], USERS[4], USERS[5]]),
]

FOLDERS = [
    domain.Folder(2025, [DOCUMENTS[0], DOCUMENTS[1]]),
    domain.Folder(2026, [DOCUMENTS[2]]),
]


def test_mapper_can_load_users(db_session: orm.Session):
    insert_users(db_session)

    expected_users = USERS

    output_users = db_session.query(domain.User).all()
    assert expected_users == output_users


def test_mapper_can_load_documents(db_session: orm.Session):
    insert_users(db_session)
    insert_documents(db_session)

    expected_documents = DOCUMENTS

    output_documents = db_session.query(domain.Document).all()
    assert expected_documents == output_documents


def test_mapper_can_load_folders(db_session: orm.Session):
    insert_users(db_session)
    insert_documents(db_session)
    insert_folders(db_session)

    expected_folders = FOLDERS

    output_folders = db_session.query(domain.Folder).all()
    assert expected_folders == output_folders
