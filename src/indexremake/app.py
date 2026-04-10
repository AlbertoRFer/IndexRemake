from PySide6 import QtQml

from indexremake import resources_rc  # noqa: F401
from indexremake.bridge.presenters import main_presenter  # noqa: F401


class IndexApp:
    def __init__(self):
        self.engine = QtQml.QQmlApplicationEngine()
        self.engine.loadFromModule("com.indexremake", "MainWindow")
