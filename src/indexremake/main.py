import sys

from PySide6 import QtWidgets

from indexremake import bootstrap
from indexremake.infrastructure.persistence import database

if __name__ == "__main__":
    qapp = QtWidgets.QApplication()
    qapp.styleHints().setWheelScrollLines(15)

    db = database.SQLiteDatabase("indexremake.db")
    index_app = bootstrap.create_index_app(db)

    exit_code = qapp.exec()

    db.dispose()
    sys.exit(exit_code)
