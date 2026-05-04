import pytest
from sqlalchemy import orm

from indexremake import domain, dtos
from indexremake.infrastructure.persistence import queries


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
        domain.Folder(2027, []),
    ]


@pytest.fixture
def db_with_data(db_session: orm.Session, folders: list[domain.Folder]) -> orm.Session:
    db_session.add_all(folders)
    db_session.commit()
    return db_session


@pytest.fixture
def document_summary_dtos(
    documents: list[domain.Document],
) -> list[dtos.DocumentSummaryDTO]:
    return [
        dtos.DocumentSummaryDTO(
            doc.document_number,
            doc.title,
            doc.users[0].first_name,
            doc.users[0].middle_name,
            doc.users[0].last_name1,
            doc.users[0].last_name2,
            len(doc.users),
        )
        for doc in documents[:2]
    ]


def test_query_can_return_only_documents_for_a_given_year(
    db_with_data: orm.Session,
    document_summary_dtos: list[dtos.DocumentSummaryDTO],
) -> None:

    fetched_docs = queries.get_documents_per_year(db_with_data, 2025)

    assert len(document_summary_dtos) == len(fetched_docs)
    assert document_summary_dtos == fetched_docs


def test_query_returns_empty_list_if_no_documents_for_a_given_year(
    db_with_data: orm.Session,
) -> None:

    fetched_docs = queries.get_documents_per_year(db_with_data, 2027)

    assert len(fetched_docs) == 0


def test_query_returns_empty_list_for_an_unknown_year(
    db_with_data: orm.Session,
) -> None:

    fetched_docs = queries.get_documents_per_year(db_with_data, 9999)

    assert len(fetched_docs) == 0
