from indexremake import dtos
from indexremake.infrastructure.persistence import database, queries


class DocumentService:
    def __init__(self, db: database.SQLiteDatabase):
        self._db = db

    def get_document_summaries_for_year(
        self, year: int
    ) -> list[dtos.DocumentSummaryDTO]:
        return queries.get_documents_per_year(self._db.get_session(), year)
