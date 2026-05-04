import sqlalchemy as sa
from sqlalchemy import orm

from indexremake import dtos
from indexremake.infrastructure.persistence.database import tables


def _to_document_summary_dto(
    row: sa.Row[tuple[int, str, str, str, str, str, int]],
) -> dtos.DocumentSummaryDTO:
    return dtos.DocumentSummaryDTO(
        row.document_number,
        row.title,
        row.first_name,
        row.middle_name,
        row.last_name1,
        row.last_name2,
        row.users_per_document,
    )


def get_documents_per_year(
    db_session: orm.Session, year: int
) -> list[dtos.DocumentSummaryDTO]:
    user_count_subquery = (
        sa.select(sa.func.count(tables.users.c.id))
        .where(tables.users.c.document_id == tables.documents.c.id)
        .scalar_subquery()
        .correlate(tables.documents)
    )

    main_query = (
        sa.select(
            tables.documents.c.document_number,
            tables.documents.c.title,
            tables.users.c.first_name,
            tables.users.c.middle_name,
            tables.users.c.last_name1,
            tables.users.c.last_name2,
            (user_count_subquery).label("users_per_document"),
        )
        .join(
            tables.folders,
            tables.documents.c.folder_id == tables.folders.c.id,
        )
        .join(
            tables.users,
            tables.users.c.document_id == tables.documents.c.id,
        )
        .where(tables.folders.c.year == year)
        .where(tables.users.c.position == 0)
        .order_by(tables.documents.c.document_number)
    )

    rows = db_session.execute(main_query).all()
    return [_to_document_summary_dto(row) for row in rows]
