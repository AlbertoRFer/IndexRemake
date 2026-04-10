import os
import typing

import pytest
from PySide6 import QtCore

from indexremake import app

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


@pytest.fixture
def index_app(qapp) -> app.IndexApp:
    return app.IndexApp()


def test_app_can_be_constructed(qapp) -> None:
    new_app = app.IndexApp()


def test_engine_can_load(index_app) -> None:
    assert index_app.engine.rootObjects()


def _find_object(root: QtCore.QObject, object_name: str) -> QtCore.QObject:
    obj = root.findChild(QtCore.QObject, object_name)

    if obj is None:
        raise RuntimeError(f"{object_name} not found — check objectName in QML")

    return obj


def test_document_list_content_can_be_retrieved(index_app) -> None:
    root = index_app.engine.rootObjects()[0]
    documents_list = _find_object(root, "documentsList")
    documents_list_model = typing.cast(
        QtCore.QAbstractItemModel, documents_list.property("model")
    )

    assert documents_list_model.rowCount() == 0
