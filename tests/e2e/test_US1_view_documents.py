import pytest

from tests.support import data, factories, pages


@pytest.fixture
def seed_data() -> list[factories.FolderData]:
    return data.load_test_data()


def test_documents_can_be_viewed(
    seed_data: list[factories.FolderData], main_page: pages.MainPage
) -> None:
    # Given a protocol with several documents
    folder_2025 = seed_data[0]
    seeded_summaries = factories.build_document_summaries(folder_2025["documents"])

    # When the aplication loads (handled by fixtures)
    # TODO: year selection not implemented yet, so we just use the first year

    # Then the documents can be viewed
    for expected_summary, retrieved_summary in zip(
        seeded_summaries, main_page.document_summaries, strict=True
    ):
        assert expected_summary.number == retrieved_summary.number
        assert expected_summary.title == retrieved_summary.title
        assert expected_summary.user_count == retrieved_summary.user_count
        assert expected_summary.user_full_name == retrieved_summary.user_full_name
