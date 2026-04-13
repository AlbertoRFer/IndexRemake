import sqlalchemy as sa

from indexremake.infrastructure.persistence import base

folders_table = sa.Table(
    "folders",
    base.metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("year", sa.Integer),
)

documents_table = sa.Table(
    "documents",
    base.metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("folder_id", sa.Integer, sa.ForeignKey("folders.id")),
    sa.Column("document_number", sa.Integer),
    sa.Column("title", sa.String),
)

users_table = sa.Table(
    "users",
    base.metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("document_id", sa.Integer, sa.ForeignKey("documents.id")),
    sa.Column("position", sa.Integer),
    sa.Column("first_name", sa.String),
    sa.Column("middle_name", sa.String),
    sa.Column("last_name1", sa.String),
    sa.Column("last_name2", sa.String),
)
