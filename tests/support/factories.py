from typing import TypedDict

import sqlalchemy as sa
from sqlalchemy import orm

from indexremake import domain, dtos
from indexremake.infrastructure.persistence.database import tables


class UserData(TypedDict):
    first_name: str
    middle_name: str | None
    last_name1: str
    last_name2: str | None


class DocumentData(TypedDict):
    number: int
    title: str
    users: list[UserData]


class FolderData(TypedDict):
    year: int
    documents: list[DocumentData]


def insert_folder_data_into_db(
    db_session: orm.Session, folder_data: list[FolderData]
) -> None:
    for folder in folder_data:
        stmt = sa.insert(tables.folders).values(year=folder["year"])
        result = db_session.execute(stmt)
        folder_id = result.inserted_primary_key[0]  # type: ignore
        insert_document_data_into_db(db_session, folder["documents"], folder_id)

    db_session.commit()


def insert_document_data_into_db(
    db_session: orm.Session, document_data: list[DocumentData], folder_id: int
) -> None:
    for document in document_data:
        stmt = sa.insert(tables.documents).values(
            folder_id=folder_id,
            number=document["number"],
            title=document["title"],
        )
        result = db_session.execute(stmt)
        document_id = result.inserted_primary_key[0]  # type: ignore

        insert_user_data_into_db(db_session, document["users"], document_id)


def insert_user_data_into_db(
    db_session: orm.Session, user_data: list[UserData], document_id: int
) -> None:
    for user_position, user in enumerate(user_data):
        stmt = sa.insert(tables.users).values(
            document_id=document_id,
            position=user_position,
            first_name=user["first_name"],
            middle_name=user["middle_name"],
            last_name1=user["last_name1"],
            last_name2=user["last_name2"],
        )
        db_session.execute(stmt)


def build_folders(folder_data: list[FolderData]) -> list[domain.Folder]:
    return [
        domain.Folder(
            year=folder["year"],
            documents=build_documents(folder["documents"]),
        )
        for folder in folder_data
    ]


def build_documents(document_data: list[DocumentData]) -> list[domain.Document]:
    return [
        domain.Document(
            number=document["number"],
            title=document["title"],
            users=build_users(document["users"]),
        )
        for document in document_data
    ]


def build_users(user_data: list[UserData]) -> list[domain.User]:
    return [
        domain.User(
            first_name=user["first_name"],
            middle_name=user["middle_name"],
            last_name1=user["last_name1"],
            last_name2=user["last_name2"],
        )
        for user in user_data
    ]


def build_document_summaries(
    document_data: list[DocumentData],
) -> list[dtos.DocumentSummaryDTO]:
    return [
        dtos.DocumentSummaryDTO(
            number=document["number"],
            title=document["title"],
            number_of_users=len(document["users"]),
            user_first_name=document["users"][0]["first_name"],
            user_middle_name=document["users"][0]["middle_name"],
            user_last_name1=document["users"][0]["last_name1"],
            user_last_name2=document["users"][0]["last_name2"],
        )
        for document in document_data
    ]
