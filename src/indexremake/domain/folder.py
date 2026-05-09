import attrs

from indexremake.domain import document


@attrs.define(slots=False)
class Folder:
    year: int
    documents: list[document.Document]
