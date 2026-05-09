import attrs


@attrs.define(slots=False)
class User:
    first_name: str
    middle_name: str | None
    last_name1: str
    last_name2: str | None
