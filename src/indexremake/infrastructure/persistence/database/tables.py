import sqlalchemy as sa

metadata = sa.MetaData()

folders = sa.Table(
    "folders",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("year", sa.Integer),
)

documents = sa.Table(
    "documents",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("folder_id", sa.Integer, sa.ForeignKey("folders.id")),
    sa.Column("document_number", sa.Integer),
    sa.Column("title", sa.String),
)

users = sa.Table(
    "users",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("document_id", sa.Integer, sa.ForeignKey("documents.id")),
    sa.Column("position", sa.Integer),
    sa.Column("first_name", sa.String),
    sa.Column("middle_name", sa.String),
    sa.Column("last_name1", sa.String),
    sa.Column("last_name2", sa.String),
)
