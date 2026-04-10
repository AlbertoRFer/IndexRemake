import os
import typing

import pytest
from PySide6 import QtCore

from indexremake import app
from tests import testing_utils

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


@pytest.fixture
def index_app(qapp) -> app.IndexApp:
    return app.IndexApp()


def test_app_can_be_constructed(qapp) -> None:
    new_app = app.IndexApp()


def test_engine_can_load(index_app) -> None:
    assert index_app.engine.rootObjects()


@pytest.fixture
def main_page(index_app) -> testing_utils.MainPage:
    return testing_utils.MainPage(index_app.engine.rootObjects()[0])


def test_document_list_content_can_be_retrieved(main_page) -> None:
    documents = main_page.documents_in_list

    assert len(documents) == 0
