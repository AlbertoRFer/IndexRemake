import typing

import attrs
import pytest
import sqlalchemy as sa
from sqlalchemy import orm

from indexremake import domain
from indexremake.infrastructure.persistence import database
from tests.support import data, factories


@pytest.fixture
def seed_data() -> list[factories.FolderData]:
    return data.load_test_data()


@pytest.fixture
def folders(seed_data: list[factories.FolderData]) -> list[domain.Folder]:
    return factories.build_folders(seed_data)


def test_mapper_can_load_domain_objects(
    seeded_db: database.SQLiteDatabase,
    folders: list[domain.Folder],
) -> None:
    # Given a database with several users, documents and folders
    session = seeded_db.get_session()

    # When we load the objects
    output_data = session.query(domain.Folder).all()

    # Then we get the objects with the correct data
    assert folders == output_data


def fetch_document_data_from_db(
    db_session: orm.Session,
) -> typing.Sequence[sa.Row[typing.Any]]:
    return db_session.execute(
        sa.text("""
        SELECT
            documents.number,
            documents.title,
            users.position,
            users.first_name,
            users.middle_name,
            users.last_name1,
            users.last_name2
        FROM documents
        JOIN users ON users.document_id == documents.id
        ORDER BY documents.number, users.position
    """)
    ).fetchall()


def test_mapper_can_save_documents_with_users(
    db: database.SQLiteDatabase,
    folders: list[domain.Folder],
) -> None:
    # Given a document with users
    session = db.get_session()
    saved_document = folders[1].documents[0]

    # When we save it into the db
    session.add(folders[1])  # Only one document gets saved
    session.commit()

    # Then the data in the db matches the data of the saved domain object
    rows = fetch_document_data_from_db(session)

    assert saved_document.number == rows[0].number
    assert saved_document.title == rows[0].title

    for user, row in zip(saved_document.users, rows, strict=True):
        row_tuple = (row.first_name, row.middle_name, row.last_name1, row.last_name2)
        assert attrs.astuple(user) == row_tuple


def fetch_folder_data_from_db(
    db_session: orm.Session,
) -> typing.Sequence[sa.Row[typing.Any]]:
    return db_session.execute(
        sa.text("""
        SELECT
            folders.year,
            documents.number,
            documents.title
        FROM folders
        JOIN documents ON documents.folder_id == folders.id
        ORDER BY folders.year, documents.number
    """)
    ).fetchall()


def test_mapper_can_save_folder_with_documents(
    db: database.SQLiteDatabase, folders: list[domain.Folder]
) -> None:
    # Given a folder with documents
    saved_folder = folders[0]
    session = db.get_session()

    # When we save it into the db
    session.add(saved_folder)
    session.commit()

    # Then the data in the db matches the data of the saved domain object
    rows = fetch_folder_data_from_db(session)

    assert saved_folder.year == rows[0].year

    assert len(rows) == 2
    assert all(saved_folder.year == row.year for row in rows)

    for document, row in zip(saved_folder.documents, rows, strict=True):
        assert document.number == row.number
        assert document.title == row.title
