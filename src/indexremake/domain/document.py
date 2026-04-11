import attrs

from indexremake.domain import user


@attrs.define(slots=False)
class Document:
    document_number: int
    title: str
    users: list[user.User]
