import typing

import attrs
from PySide6 import QtCore


def _find_object(root: QtCore.QObject, object_name: str) -> QtCore.QObject:
    obj = root.findChild(QtCore.QObject, object_name)

    if obj is None:
        raise RuntimeError(f"{object_name} not found — check objectName in QML")

    return obj


@attrs.define
class MainPage:
    _root: QtCore.QObject
    _documents_list: QtCore.QObject = attrs.field(init=False)

    def __attrs_post_init__(self):
        self._documents_list = _find_object(self._root, "documentsList")

    @property
    def documents_in_list(self) -> list[str]:
        model = typing.cast(
            QtCore.QAbstractItemModel, self._documents_list.property("model")
        )

        documents = []
        for i in range(model.rowCount()):
            documents_data = model.data(
                model.index(i, 0), QtCore.Qt.ItemDataRole.DisplayRole
            )
            documents.append(documents_data)

        return documents
