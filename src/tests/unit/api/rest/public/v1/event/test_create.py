from http import HTTPStatus
from typing import Any
from unittest.mock import AsyncMock

import pytest
from _pytest.fixtures import SubRequest
from fastapi import FastAPI
from httpx import AsyncClient
from pytest_mock import MockerFixture

from app.app_layer.use_cases.event.create_event import CreateEventUseCase
from app.app_layer.use_cases.event.dto import EventOutputDTO
from app.domain.event.value_objects import EventStatusEnum, EventTypeEnum
from app.domain.interfaces.repositories.event.exceptions import ActiveEventAlreadyExistsError
from tests.utils import fake


@pytest.fixture()
def url_path() -> str:
    return "api/v1/event"


@pytest.fixture()
def use_case(request: SubRequest, mocker: MockerFixture) -> AsyncMock:
    mock = mocker.AsyncMock(spec=CreateEventUseCase)

    if "returns" in request.param:
        mock.create_event.return_value = request.param["returns"]
    elif "raises" in request.param:
        mock.create_event.side_effect = request.param["raises"]

    return mock


@pytest.fixture()
def application(application: FastAPI, use_case: AsyncMock) -> FastAPI:
    with application.container.create_event_use_case.override(use_case):
        yield application


@pytest.mark.parametrize(
    "use_case",
    [
        {
            "returns": EventOutputDTO(
                id=fake.cryptographic.uuid_object(),
                coefficient=2.22,
                deadline=fake.datetime.datetime(),
                status=EventStatusEnum.UNFINISHED,
                type=EventTypeEnum.NONE,
                info=""
            ),
        }
    ],
    indirect=True,
)
async def test_ok(http_client: AsyncClient, use_case: AsyncMock, url_path: str) -> None:
    response = await http_client.post(url=url_path)

    assert response.status_code == HTTPStatus.OK, f"Unexpected response: {response.text}"
    expected_data = {
        "id": str(use_case.create_event.return_value.id),
        "coefficient": float(use_case.create_event.return_value.coefficient),
        "deadline":use_case.create_event.return_value.deadline,
        "status":use_case.create_event.return_value.status,
        "type":use_case.create_event.return_value.type,
        "info":use_case.create_event.return_value.info
    }
    assert response.json() == expected_data, (
        f"Response JSON does not match expected data.\n"
        f"Expected: {expected_data}\n"
        f"Actual: {response.json()}"
    )


@pytest.mark.parametrize(
    ("use_case", "expected_code", "expected_error"),
    [
        pytest.param(
            {"raises": ActiveEventAlreadyExistsError},
            HTTPStatus.BAD_REQUEST,
            {"detail": {"code": 2001, "message": "Active event already exists."}},
            id="ACTIVE_EVENT_ALREADY_EXISTS",
        ),
    ],
    indirect=["use_case"],
)
async def test_failed(
    http_client: AsyncClient,
    use_case: AsyncMock,
    url_path: str,
    expected_code: int,
    expected_error: dict[str, Any],
) -> None:
    response = await http_client.post(url=url_path)

    assert response.status_code == expected_code, response.text
    assert response.json() == expected_error
