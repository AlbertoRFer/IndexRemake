from PySide6 import QtCore, QtQml

QML_IMPORT_NAME = "com.indexremake"
QML_IMPORT_MAJOR_VERSION = 1


class MainPresenter(QtCore.QObject):
    def __init__(self, parent: QtCore.QObject | None = None):
        super().__init__(parent)

        self._documents_list_model = QtCore.QStringListModel([])

    @QtCore.Property(QtCore.QAbstractItemModel, constant=True)
    def documentsListModel(self) -> QtCore.QAbstractItemModel:
        return self._documents_list_model


QtQml.QmlElement(MainPresenter)
