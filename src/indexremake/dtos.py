import attrs


def format_full_name(
    first_name: str, middle_name: str | None, last_name1: str, last_name2: str | None
) -> str:
    last = f"{last_name1} {last_name2}" if last_name2 else last_name1
    first = f"{first_name} {middle_name}" if middle_name else first_name

    return f"{last}, {first}"


@attrs.define(frozen=True)
class DocumentSummaryDTO:
    number: int
    title: str
    user_count: int
    user_full_name: str
