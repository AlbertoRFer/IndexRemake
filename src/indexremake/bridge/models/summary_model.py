import enum
import typing

from PySide6 import QtCore

from indexremake import dtos


class DocumentSummaryModel(QtCore.QAbstractListModel):
    class Role(enum.IntEnum):
        Number = QtCore.Qt.ItemDataRole.UserRole
        Title = QtCore.Qt.ItemDataRole.UserRole + 1
        NumberOfUsers = QtCore.Qt.ItemDataRole.UserRole + 2
        UserFirstName = QtCore.Qt.ItemDataRole.UserRole + 3
        UserMiddleName = QtCore.Qt.ItemDataRole.UserRole + 4
        UserLastName1 = QtCore.Qt.ItemDataRole.UserRole + 5
        UserLastName2 = QtCore.Qt.ItemDataRole.UserRole + 6

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
            return summary.number_of_users

        if role == self.Role.UserFirstName:
            return summary.user_first_name

        if role == self.Role.UserMiddleName:
            return summary.user_middle_name

        if role == self.Role.UserLastName1:
            return summary.user_last_name1

        if role == self.Role.UserLastName2:
            return summary.user_last_name2

    def roleNames(self) -> dict[int, QtCore.QByteArray]:
        roles = super().roleNames()
        roles[self.Role.Number] = QtCore.QByteArray(b"number")
        roles[self.Role.Title] = QtCore.QByteArray(b"title")
        roles[self.Role.NumberOfUsers] = QtCore.QByteArray(b"numberOfUsers")
        roles[self.Role.UserFirstName] = QtCore.QByteArray(b"userFirstName")
        roles[self.Role.UserMiddleName] = QtCore.QByteArray(b"userMiddleName")
        roles[self.Role.UserLastName1] = QtCore.QByteArray(b"userLastName1")
        roles[self.Role.UserLastName2] = QtCore.QByteArray(b"userLastName2")

        return roles
