import sqlalchemy as sa
from sqlalchemy import event, orm

from indexremake.infrastructure.persistence.database import base, mappings


class SQLiteDatabase:
    def __init__(self, db_path: str) -> None:
        self._create_engine(db_path)

        self._session_maker = orm.sessionmaker(bind=self._engine)

    def _create_engine(self, db_path: str) -> None:
        self._engine = sa.create_engine(f"sqlite:///{db_path}")

        @event.listens_for(self._engine, "connect")
        def enable_foreign_keys(dbapi_connection, _):
            dbapi_connection.execute("PRAGMA foreign_keys=ON")

    def create_all(self) -> None:
        base.metadata.create_all(self._engine)

    def get_session(self) -> orm.Session:
        return self._session_maker()
