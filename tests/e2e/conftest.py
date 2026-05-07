import pytest
from PySide6 import QtWidgets

from indexremake import app, bootstrap
from indexremake.infrastructure.persistence import database
from tests.support import pages


@pytest.fixture
def index_app(
    qapp: QtWidgets.QApplication, seeded_db: database.SQLiteDatabase
) -> app.IndexApp:
    return bootstrap.create_index_app(seeded_db)


@pytest.fixture
def main_page(index_app: app.IndexApp) -> pages.MainPage:
    return pages.MainPage(index_app.engine.rootObjects()[0])
