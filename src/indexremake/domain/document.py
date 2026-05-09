import attrs

from indexremake.domain import user


@attrs.define(slots=False)
class Document:
    number: int
    title: str
    users: list[user.User]
