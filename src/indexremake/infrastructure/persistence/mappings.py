from sqlalchemy import orm

from indexremake import domain
from indexremake.infrastructure.persistence import base, tables


def start_mappers() -> None:
    base.mapper_registry.map_imperatively(domain.User, tables.users_table)
    base.mapper_registry.map_imperatively(
        domain.Document,
        tables.documents_table,
        properties={
            "users": orm.relationship(
                domain.User, order_by=tables.users_table.c.position
            )
        },
    )
    base.mapper_registry.map_imperatively(
        domain.Folder,
        tables.folders_table,
        properties={
            "documents": orm.relationship(
                domain.Document, order_by=tables.documents_table.c.document_number
            )
        },
    )
