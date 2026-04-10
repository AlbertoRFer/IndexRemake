from PySide6 import QtCore, QtQml

QML_IMPORT_NAME = "com.indexremake"
QML_IMPORT_MAJOR_VERSION = 1


class MainPresenter(QtCore.QObject):
    _instance: MainPresenter | None = None

    def __init__(self, doc_list: list[str], parent: QtCore.QObject | None = None):
        super().__init__(parent)

        self._documents_list_model = QtCore.QStringListModel(doc_list)

    @QtCore.Property(QtCore.QAbstractItemModel, constant=True)
    def documentsListModel(self) -> QtCore.QAbstractItemModel:
        return self._documents_list_model

    @staticmethod
    def set_instance(instance: MainPresenter) -> None:
        MainPresenter._instance = instance

    @staticmethod
    def create(engine) -> MainPresenter:
        if MainPresenter._instance is not None:
            return MainPresenter._instance

        raise RuntimeError("MainPresenter not initialized")


QtQml.QmlSingleton(MainPresenter)
QtQml.QmlElement(MainPresenter)
