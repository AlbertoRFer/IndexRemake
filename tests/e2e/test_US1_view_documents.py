import pytest

from tests.support import data, factories, pages


@pytest.fixture
def seed_data() -> list[factories.FolderData]:
    return data.load_test_data()


def test_documents_can_be_viewed(
    seed_data: list[factories.FolderData], main_page: pages.MainPage
) -> None:
    # Given a protocol with several documents
    document_data = [doc["title"] for doc in seed_data[0]["documents"]]

    # When the aplication loads (handled by fixtures)

    # Then the documents can be viewed
    assert document_data == main_page.documents_in_list
