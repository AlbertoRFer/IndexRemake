import os

import pytest

from indexremake import app
from tests.support import pages

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


@pytest.fixture
def doc_list() -> list[str]:
    return ["Document1", "Document2", "Document3"]


@pytest.fixture
def index_app(qapp, doc_list) -> app.IndexApp:
    return app.IndexApp(doc_list)


@pytest.fixture
def main_page(index_app) -> pages.MainPage:
    return pages.MainPage(index_app.engine.rootObjects()[0])


def test_document_list_content_can_be_retrieved(main_page, doc_list) -> None:
    documents = main_page.documents_in_list

    for expected_doc, output_doc in zip(doc_list, documents, strict=True):
        assert expected_doc == output_doc
