import sqlite3

import sqlalchemy as sa
from sqlalchemy import event, orm

from indexremake.infrastructure.persistence.database import base, mappings


class SQLiteDatabase:
    def __init__(self, db_path: str) -> None:
        self._create_engine(db_path)

        mappings.start_mappers()
        base.metadata.create_all(self._engine)

        self._Session = orm.sessionmaker(bind=self._engine)

    def _create_engine(self, db_path: str) -> None:
        self._engine = sa.create_engine(f"sqlite:///{db_path}")
        event.listen(self._engine, "connect", self._enable_foreign_keys)

    @staticmethod
    def _enable_foreign_keys(
        dbapi_connection: sqlite3.Connection, _: sa.pool.ConnectionPoolEntry
    ) -> None:
        dbapi_connection.execute("PRAGMA foreign_keys=ON")

    def get_session(self) -> orm.Session:
        return self._Session()

    def dispose(self) -> None:
        self._engine.dispose()
