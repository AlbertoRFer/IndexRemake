import sqlalchemy as sa
from sqlalchemy import orm

from indexremake import dtos
from indexremake.infrastructure.persistence.database import tables


def _to_document_summary_dto(
    row: sa.Row[tuple[int, str, str, str, str, str, int]],
) -> dtos.DocumentSummaryDTO:
    return dtos.DocumentSummaryDTO(
        number=row.number,
        title=row.title,
        user_count=row.users_per_document,
        user_full_name=dtos.format_full_name(
            row.first_name, row.middle_name, row.last_name1, row.last_name2
        ),
    )


def get_documents_per_year(
    db_session: orm.Session, year: int
) -> list[dtos.DocumentSummaryDTO]:
    temp_table = (
        sa.select(
            tables.users.c.document_id,
            sa.func.count(tables.users.c.id).label("users_per_document"),
        )
        .group_by(tables.users.c.document_id)
        .subquery()
    )

    main_query = (
        sa.select(
            tables.documents.c.number,
            tables.documents.c.title,
            tables.users.c.first_name,
            tables.users.c.middle_name,
            tables.users.c.last_name1,
            tables.users.c.last_name2,
            temp_table.c.users_per_document,
        )
        .join(
            tables.folders,
            tables.documents.c.folder_id == tables.folders.c.id,
        )
        .join(
            tables.users,
            tables.users.c.document_id == tables.documents.c.id,
        )
        .join(temp_table, temp_table.c.document_id == tables.documents.c.id)
        .where(tables.folders.c.year == year)
        .where(tables.users.c.position == 0)
        .order_by(tables.documents.c.number)
    )

    rows = db_session.execute(main_query).all()
    return [_to_document_summary_dto(row) for row in rows]
