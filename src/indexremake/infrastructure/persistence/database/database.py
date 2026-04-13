import sqlalchemy as sa
from sqlalchemy import orm

from indexremake.infrastructure.persistence.database import base, mappings


class Database:
    def __init__(self, db_path: str) -> None:
        self._engine = sa.create_engine(f"sqlite:///{db_path}")
        self._session_maker = orm.sessionmaker(bind=self._engine)

    def create_all(self) -> None:
        base.metadata.create_all(self._engine)

    def get_session(self) -> orm.Session:
        return self._session_maker()
