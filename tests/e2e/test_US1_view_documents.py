import json
import pathlib

import pytest

from indexremake import app
from tests.support import pages

DATA_PATH = pathlib.Path(__file__).parent / "test_data" / "document_data.json"


@pytest.fixture
def document_data() -> list[dict]:
    with DATA_PATH.open() as f:
        return json.load(f)


@pytest.fixture
def index_app(qapp, doc_list) -> app.IndexApp:
    return app.IndexApp(doc_list)


@pytest.fixture
def main_page(index_app) -> pages.MainPage:
    return pages.MainPage(index_app.engine.rootObjects()[0])


def test_documents_can_be_viewed(
    document_data: list[dict], main_page: pages.MainPage
) -> None:
    # Given a protocol with several documents

    # When the aplication loads (handled by fixtures)

    # Then the documents can be viewed
    for expected_document, output_document in zip(
        document_data, main_page.documents_in_list, strict=True
    ):
        assert expected_document == output_document
