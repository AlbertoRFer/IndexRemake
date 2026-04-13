from sqlalchemy import orm

from indexremake import domain
from indexremake.infrastructure.persistence.database import base, tables


def start_mappers() -> None:
    if base.mapper_registry.mappers:
        return

    base.mapper_registry.map_imperatively(domain.User, tables.users)
    base.mapper_registry.map_imperatively(
        domain.Document,
        tables.documents,
        properties={
            "users": orm.relationship(domain.User, order_by=tables.users.c.position)
        },
    )
    base.mapper_registry.map_imperatively(
        domain.Folder,
        tables.folders,
        properties={
            "documents": orm.relationship(
                domain.Document, order_by=tables.documents.c.document_number
            )
        },
    )
