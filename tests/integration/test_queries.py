import pytest
import pytest_cases

from indexremake import dtos
from indexremake.infrastructure.persistence import database, queries
from tests.support import data, factories


@pytest.fixture
def seed_data() -> list[factories.FolderData]:
    return data.load_test_data()


@pytest.fixture
def summaries_2025(
    seed_data: list[factories.FolderData],
) -> list[dtos.DocumentSummaryDTO]:
    folder_data_2025 = seed_data[0]

    return factories.build_document_summaries(folder_data_2025["documents"])


def test_query_can_return_documents_for_a_given_year(
    seeded_db: database.SQLiteDatabase,
    summaries_2025: list[dtos.DocumentSummaryDTO],
) -> None:
    session = seeded_db.get_session()

    fetched_docs = queries.get_documents_per_year(session, 2025)

    assert len(summaries_2025) == len(fetched_docs)
    assert summaries_2025 == fetched_docs


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
