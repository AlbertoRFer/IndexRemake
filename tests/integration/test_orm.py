import typing

import attrs
import pytest
import sqlalchemy as sa
from sqlalchemy import orm

from indexremake import domain


# db_session needs to run first so the mappers are called
# before creating the domain objects
@pytest.fixture
def users(db_session: orm.Session) -> list[domain.User]:
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
def db_with_users(db_session: orm.Session) -> orm.Session:
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


@pytest.fixture
def db_with_documents_and_users(db_with_users: orm.Session) -> orm.Session:
    db_with_users.execute(
        sa.text("""
        INSERT INTO documents (folder_id, document_number, title)
        VALUES
            (1, 1, 'Document 1'),
            (1, 2, 'Document 2'),
            (2, 3, 'Document 3')
        """)
    )
    return db_with_users


@pytest.fixture
def db_with_folders_documents_and_users(
    db_with_documents_and_users: orm.Session,
) -> orm.Session:
    db_with_documents_and_users.execute(
        sa.text("""
        INSERT INTO folders (year)
        VALUES
            (2025),
            (2026)
        """)
    )
    return db_with_documents_and_users


def test_mapper_can_load_users(
    db_with_users: orm.Session, users: list[domain.User]
) -> None:
    expected_users = users

    output_users = db_with_users.query(domain.User).all()
    assert expected_users == output_users


def test_mapper_can_load_documents(
    db_with_documents_and_users: orm.Session, documents: list[domain.Document]
) -> None:
    expected_documents = documents

    output_documents = db_with_documents_and_users.query(domain.Document).all()
    assert expected_documents == output_documents


def test_mapper_can_load_folders(
    db_with_folders_documents_and_users: orm.Session, folders: list[domain.Folder]
) -> None:
    expected_folders = folders

    output_folders = db_with_folders_documents_and_users.query(domain.Folder).all()
    assert expected_folders == output_folders


def fetch_user_data_from_db(
    db_session: orm.Session,
) -> typing.Sequence[sa.Row[typing.Any]]:
    return list(
        db_session.execute(
            sa.text("""
            SELECT
                users.first_name,
                users.middle_name,
                users.last_name1,
                users.last_name2
            FROM users
            ORDER BY users.document_id, users.position
            """)
        ).fetchall()
    )


def test_mapper_can_save_users(
    db_session: orm.Session, users: list[domain.User]
) -> None:
    for user in users:
        db_session.add(user)
    db_session.commit()

    output_data = fetch_user_data_from_db(db_session)
    expected_data = [attrs.astuple(user) for user in users]
    for expected_user, output_user in zip(expected_data, output_data, strict=True):
        assert expected_user == output_user


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


def test_mapper_can_save_documents(
    db_session: orm.Session, documents: list[domain.Document]
) -> None:
    document_to_save = documents[0]

    db_session.add(document_to_save)
    db_session.commit()

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


def test_mapper_can_save_folder(
    db_session: orm.Session, folders: list[domain.Folder]
) -> None:
    folder_to_save = folders[0]

    db_session.add(folder_to_save)
    db_session.commit()

    rows = fetch_folder_data_from_db(db_session)

    assert folder_to_save.year == rows[0].year

    assert len(rows) == 2
    assert all(folder_to_save.year == row.year for row in rows)

    for document, row in zip(folder_to_save.documents, rows, strict=True):
        assert document.document_number == row.document_number
        assert document.title == row.title
