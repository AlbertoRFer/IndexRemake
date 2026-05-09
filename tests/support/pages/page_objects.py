import typing

import attrs
from PySide6 import QtCore

from indexremake import dtos
from indexremake.bridge import models


def _find_object(root: QtCore.QObject, object_name: str) -> QtCore.QObject:
    obj = root.findChild(QtCore.QObject, object_name)

    if obj is None:
        raise RuntimeError(f"{object_name} not found — check objectName in QML")

    return obj


@attrs.define
class MainPage:
    _root: QtCore.QObject
    _documents_list: QtCore.QObject = attrs.field(init=False)

    def __attrs_post_init__(self) -> None:
        self._documents_list = _find_object(self._root, "docSummaryList")

    @property
    def document_summaries(self) -> list[dtos.DocumentSummaryDTO]:
        model = typing.cast(
            models.DocumentSummaryModel, self._documents_list.property("model")
        )

        summaries = []
        for i in range(model.rowCount()):
            idx = model.index(i, 0)
            summary = dtos.DocumentSummaryDTO(
                number=model.data(idx, model.Role.Number),
                title=model.data(idx, model.Role.Title),
                user_count=model.data(idx, model.Role.NumberOfUsers),
                user_full_name=model.data(idx, model.Role.UserFullName),
            )
            summaries.append(summary)

        return summaries
