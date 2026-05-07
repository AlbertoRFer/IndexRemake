import logging

from PySide6 import QtQml

from indexremake import resources_rc  # noqa: F401
from indexremake.bridge.presenters import main_presenter  # noqa: F401

logger = logging.getLogger(__name__)


class IndexApp:
    def __init__(self) -> None:
        self.engine = QtQml.QQmlApplicationEngine()
        self.engine.warnings.connect(self._on_engine_warnings)
        self.engine.loadFromModule("com.indexremake", "MainWindow")

    def _on_engine_warnings(self, warnings: list[QtQml.QQmlError]) -> None:
        for warning in warnings:
            logger.warning("QML: %s", warning.toString())
