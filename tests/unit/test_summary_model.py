import pytest

from indexremake import dtos
from indexremake.bridge import models
from tests.support import data, factories


@pytest.fixture
def test_data() -> list[factories.FolderData]:
    return data.load_test_data()


@pytest.fixture
def summaries_2025(
    test_data: list[factories.FolderData],
) -> list[dtos.DocumentSummaryDTO]:
    folder_data_2025 = test_data[0]
    return factories.build_document_summaries(folder_data_2025["documents"])


@pytest.fixture
def summaries_2026(
    test_data: list[factories.FolderData],
) -> list[dtos.DocumentSummaryDTO]:
    folder_data_2026 = test_data[1]
    return factories.build_document_summaries(folder_data_2026["documents"])


def test_empty_model_can_load_summaries(
    summaries_2025: list[dtos.DocumentSummaryDTO],
) -> None:
    model = models.DocumentSummaryModel()

    model.load_summaries(summaries_2025)

    for summary, row in zip(summaries_2025, range(model.rowCount()), strict=True):
        idx = model.index(row, 0)
        assert summary.number == model.data(idx, model.Role.Number)
        assert summary.title == model.data(idx, model.Role.Title)
        assert summary.number_of_users == model.data(idx, model.Role.NumberOfUsers)
        assert summary.user_first_name == model.data(idx, model.Role.UserFirstName)
        assert summary.user_middle_name == model.data(idx, model.Role.UserMiddleName)
        assert summary.user_last_name1 == model.data(idx, model.Role.UserLastName1)
        assert summary.user_last_name2 == model.data(idx, model.Role.UserLastName2)


def test_model_can_refresh_summaries(
    summaries_2025: list[dtos.DocumentSummaryDTO],
    summaries_2026: list[dtos.DocumentSummaryDTO],
) -> None:
    model = models.DocumentSummaryModel()
    model.load_summaries(summaries_2025)

    model.load_summaries(summaries_2026)

    for summary, row in zip(summaries_2026, range(model.rowCount()), strict=True):
        idx = model.index(row, 0)
        assert summary.number == model.data(idx, model.Role.Number)
        assert summary.title == model.data(idx, model.Role.Title)
        assert summary.number_of_users == model.data(idx, model.Role.NumberOfUsers)
        assert summary.user_first_name == model.data(idx, model.Role.UserFirstName)
        assert summary.user_middle_name == model.data(idx, model.Role.UserMiddleName)
        assert summary.user_last_name1 == model.data(idx, model.Role.UserLastName1)
        assert summary.user_last_name2 == model.data(idx, model.Role.UserLastName2)


def test_model_can_clear_summaries(
    summaries_2025: list[dtos.DocumentSummaryDTO],
) -> None:
    model = models.DocumentSummaryModel()
    model.load_summaries(summaries_2025)

    model.load_summaries([])

    assert 0 == model.rowCount()
