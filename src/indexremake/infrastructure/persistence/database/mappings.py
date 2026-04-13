from sqlalchemy import orm

from indexremake import domain
from indexremake.infrastructure.persistence.database import tables

mapper_registry = orm.registry(metadata=tables.metadata)


def start_mappers() -> None:
    mapper_registry.map_imperatively(domain.User, tables.users)
    mapper_registry.map_imperatively(
        domain.Document,
        tables.documents,
        properties={
            "users": orm.relationship(domain.User, order_by=tables.users.c.position)
        },
    )
    mapper_registry.map_imperatively(
        domain.Folder,
        tables.folders,
        properties={
            "documents": orm.relationship(
                domain.Document, order_by=tables.documents.c.document_number
            )
        },
    )
