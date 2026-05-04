import attrs


@attrs.define(frozen=True)
class DocumentSummaryDTO:
    document_number: int
    title: str
    user_first_name: str
    user_middle_name: str | None
    user_last_name1: str
    user_last_name2: str | None
    number_of_users: int
