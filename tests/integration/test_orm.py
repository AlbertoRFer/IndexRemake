import typing

import attrs
import pytest
import pytest_cases
import sqlalchemy as sa
from sqlalchemy import orm

from indexremake import domain


@pytest.fixture
def users() -> list[domain.User]:
    return [
        domain.User("John", None, "Doe", "Tre"),
        domain.User("Jane", None, "Doe", "Fire"),
        domain.User("Juan", "Eriberto", "Five", "Six of Seven"),
        domain.User("Camilo", None, "Cruz", "Pereira"),
        domain.User("Amalia", "de la Caridad", "Rodríguez", "Díaz"),
        domain.User("Marco", "Polo", "Traveller", None),
    ]


@pytest.fixture
def documents(users: list[domain.User]) -> list[domain.Document]:
    return [
        domain.Document(1, "Document 1", users[:2]),
        domain.Document(2, "Document 2", [users[2]]),
        domain.Document(3, "Document 3", users[3:]),
    ]


@pytest.fixture
def folders(documents: list[domain.Document]) -> list[domain.Folder]:
    return [
        domain.Folder(2025, documents[:2]),
        domain.Folder(2026, [documents[2]]),
    ]


@pytest.fixture
def db_with_data(db_session: orm.Session) -> orm.Session:
    db_session.execute(
        sa.text("""
        INSERT INTO folders (year)
        VALUES
            (2025),
            (2026)
        """)
    )

    db_session.execute(
        sa.text("""
        INSERT INTO documents (folder_id, document_number, title)
        VALUES
            (1, 1, 'Document 1'),
            (1, 2, 'Document 2'),
            (2, 3, 'Document 3')
        """)
    )

    db_session.execute(
        sa.text("""
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
    return db_session


@pytest_cases.parametrize(
    "domain_type, domain_objects",
    [
        (domain.User, users),
        (domain.Document, documents),
        (domain.Folder, folders),
    ],
    ids=["users", "documents", "folders"],
)
def test_mapper_can_load_domain_objects(
    db_with_data: orm.Session,
    domain_type: type[domain.User | domain.Document | domain.Folder],
    domain_objects: typing.Iterable[domain.User | domain.Document | domain.Folder],
) -> None:
    # Given a database with several users, documents and folders

    # When we load the objects
    output_data = db_with_data.query(domain_type).all()

    # Then we get the objects with the correct data
    assert domain_objects == output_data


def fetch_document_data_from_db(
    db_session: orm.Session,
) -> typing.Sequence[sa.Row[typing.Any]]:
    return db_session.execute(
        sa.text("""
        SELECT
            documents.document_number,
            documents.title,
            users.position,
            users.first_name,
            users.middle_name,
            users.last_name1,
            users.last_name2
        FROM documents
        JOIN users ON users.document_id == documents.id
        ORDER BY documents.document_number, users.position
    """)
    ).fetchall()


def test_mapper_can_save_documents_with_users(
    db_session: orm.Session, documents: list[domain.Document]
) -> None:
    # Given a document with users
    document_to_save = documents[0]
    test_folder = domain.Folder(2025, [document_to_save])

    # When we save it into the db
    db_session.add(test_folder)
    db_session.commit()

    # Then the data in the db matches the data of the saved domain object
    rows = fetch_document_data_from_db(db_session)

    assert document_to_save.document_number == rows[0].document_number
    assert document_to_save.title == rows[0].title

    for user, row in zip(document_to_save.users, rows, strict=True):
        row_tuple = (row.first_name, row.middle_name, row.last_name1, row.last_name2)
        assert attrs.astuple(user) == row_tuple


def fetch_folder_data_from_db(
    db_session: orm.Session,
) -> typing.Sequence[sa.Row[typing.Any]]:
    return db_session.execute(
        sa.text("""
        SELECT
            folders.year,
            documents.document_number,
            documents.title
        FROM folders
        JOIN documents ON documents.folder_id == folders.id
        ORDER BY folders.year, documents.document_number
    """)
    ).fetchall()


def test_mapper_can_save_folder_with_documents(
    db_session: orm.Session, folders: list[domain.Folder]
) -> None:
    # Given a folder with documents
    folder_to_save = folders[0]

    # When we save it into the db
    db_session.add(folder_to_save)
    db_session.commit()

    # Then the data in the db matches the data of the saved domain object
    rows = fetch_folder_data_from_db(db_session)

    assert folder_to_save.year == rows[0].year

    assert len(rows) == 2
    assert all(folder_to_save.year == row.year for row in rows)

    for document, row in zip(folder_to_save.documents, rows, strict=True):
        assert document.document_number == row.document_number
        assert document.title == row.title
