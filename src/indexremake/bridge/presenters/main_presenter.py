from PySide6 import QtCore, QtQml

from indexremake import services

QML_IMPORT_NAME = "com.indexremake"
QML_IMPORT_MAJOR_VERSION = 1


class MainPresenter(QtCore.QObject):
    _instance: MainPresenter | None = None

    def __init__(
        self,
        document_service: services.DocumentService,
        parent: QtCore.QObject | None = None,
    ):
        super().__init__(parent)

        self._document_service = document_service

        self._documents_list_model = QtCore.QStringListModel()

        self.update_documents_list_model()

    @QtCore.Property(QtCore.QAbstractItemModel, constant=True)
    def documentsListModel(self) -> QtCore.QAbstractItemModel:
        return self._documents_list_model

    @staticmethod
    def set_instance(instance: MainPresenter) -> None:
        MainPresenter._instance = instance

    @staticmethod
    def create(engine: QtQml.QQmlEngine) -> MainPresenter:
        if MainPresenter._instance is not None:
            return MainPresenter._instance

        raise RuntimeError("MainPresenter not initialized")

    def update_documents_list_model(self) -> None:
        documents = self._document_service.get_document_summaries_for_year(2025)
        document_titles = [doc.title for doc in documents]
        self._documents_list_model.setStringList(document_titles)


QtQml.QmlSingleton(MainPresenter)
QtQml.QmlElement(MainPresenter)
