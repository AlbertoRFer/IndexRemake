import attrs


@attrs.define(frozen=True)
class DocumentSummaryDTO:
    number: int
    title: str
    number_of_users: int
    user_first_name: str
    user_middle_name: str | None
    user_last_name1: str
    user_last_name2: str | None
