import pytest

from indexremake import app


@pytest.fixture
def index_app(qapp) -> app.IndexApp:
    return app.IndexApp()


def test_app_can_be_constructed(qapp) -> None:
    new_app = app.IndexApp()


def test_engine_can_load(index_app) -> None:
    assert index_app.engine.rootObjects()
