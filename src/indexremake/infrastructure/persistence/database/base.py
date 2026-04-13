from sqlalchemy import orm

mapper_registry = orm.registry()
metadata = mapper_registry.metadata
