import json
import pathlib
import typing

from tests.support import factories

_DATA_DIR = pathlib.Path(__file__).parent
_TEST_DATA = _DATA_DIR / "test_data" / "test_data.json"


def load_test_data() -> list[factories.FolderData]:
    with open(_TEST_DATA) as f:
        return typing.cast(list[factories.FolderData], json.load(f))
