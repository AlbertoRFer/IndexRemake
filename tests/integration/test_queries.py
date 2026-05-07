import pytest
import pytest_cases

from indexremake import domain, dtos
from indexremake.infrastructure.persistence import database, queries
from tests.support import data, factories


@pytest.fixture
def seed_data() -> list[factories.FolderData]:
    return data.load_test_data()


@pytest.fixture
def folders(seed_data: list[factories.FolderData]) -> list[domain.Folder]:
    return factories.build_folders(seed_data)


def build_summaries(
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
        for doc in documents
    ]


def test_query_can_return_documents_for_a_given_year(
    seeded_db: database.SQLiteDatabase,
    folders: list[domain.Folder],
) -> None:
    summaries = build_summaries(folders[0].documents)
    session = seeded_db.get_session()

    fetched_docs = queries.get_documents_per_year(session, 2025)

    assert len(summaries) == len(fetched_docs)
    assert summaries == fetched_docs


@pytest_cases.parametrize(
    "year", [2027, 9999], ids=["No documents for year", "No year in database"]
)
def test_query_returns_empty_list(
    seeded_db: database.SQLiteDatabase,
    year: int,
) -> None:
    session = seeded_db.get_session()

    fetched_docs = queries.get_documents_per_year(session, year)

    assert len(fetched_docs) == 0
