import sqlalchemy as sa

from indexremake.infrastructure.persistence.database import base

folders = sa.Table(
    "folders",
    base.metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True, nullable=False),
    sa.Column("year", sa.Integer, nullable=False),
)

documents = sa.Table(
    "documents",
    base.metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True, nullable=False),
    sa.Column("folder_id", sa.Integer, sa.ForeignKey("folders.id"), nullable=False),
    sa.Column("document_number", sa.Integer, nullable=False),
    sa.Column("title", sa.String, nullable=False),
)

users = sa.Table(
    "users",
    base.metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True, nullable=False),
    sa.Column("document_id", sa.Integer, sa.ForeignKey("documents.id"), nullable=False),
    sa.Column("position", sa.Integer, nullable=False),
    sa.Column("first_name", sa.String, nullable=False),
    sa.Column("middle_name", sa.String),
    sa.Column("last_name1", sa.String, nullable=False),
    sa.Column("last_name2", sa.String),
)
