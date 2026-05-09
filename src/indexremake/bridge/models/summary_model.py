import enum
import typing

from PySide6 import QtCore

from indexremake import dtos


class DocumentSummaryModel(QtCore.QAbstractListModel):
    class Role(enum.IntEnum):
        Number = QtCore.Qt.ItemDataRole.UserRole
        Title = QtCore.Qt.ItemDataRole.UserRole + 1
        NumberOfUsers = QtCore.Qt.ItemDataRole.UserRole + 2
        UserFullName = QtCore.Qt.ItemDataRole.UserRole + 3

    def __init__(self, parent: QtCore.QObject | None = None) -> None:
        super().__init__(parent)
        self._summaries: list[dtos.DocumentSummaryDTO] = []

    def rowCount(
        self,
        parent: QtCore.QModelIndex
        | QtCore.QPersistentModelIndex = QtCore.QModelIndex(),
    ) -> int:
        return len(self._summaries)

    def load_summaries(self, summaries: list[dtos.DocumentSummaryDTO]) -> None:
        self.beginResetModel()
        self._summaries = summaries
        self.endResetModel()

    def data(
        self,
        index: QtCore.QModelIndex | QtCore.QPersistentModelIndex,
        role: int = QtCore.Qt.ItemDataRole.UserRole,
    ) -> typing.Any:
        row = index.row()
        if row >= self.rowCount():
            return None

        summary = self._summaries[row]

        if role == self.Role.Number:
            return summary.number

        if role == self.Role.Title:
            return summary.title

        if role == self.Role.NumberOfUsers:
            return summary.user_count

        if role == self.Role.UserFullName:
            return summary.user_full_name

    def roleNames(self) -> dict[int, QtCore.QByteArray]:
        roles = super().roleNames()
        roles[self.Role.Number] = QtCore.QByteArray(b"number")
        roles[self.Role.Title] = QtCore.QByteArray(b"title")
        roles[self.Role.NumberOfUsers] = QtCore.QByteArray(b"userCount")
        roles[self.Role.UserFullName] = QtCore.QByteArray(b"userFullName")

        return roles
