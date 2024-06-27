import base64

import pytest
import sqlalchemy as sa
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from models import db_models as m


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "auth_provided, auth_correct",
    (
        (True, True),  # is_authed()
        (False, False),  # is_not_authed()
        (True, False),  # login_or_password_incorrect()
    ),
    ids=(
        "is_authed",
        "is_not_authed",
        "login_or_password_incorrect",
    ),
)
async def test_auth(
    dbsession: AsyncSession,
    test_client_rest: AsyncClient,
    auth_token,
    auth_provided,
    auth_correct,
):
    if not auth_provided:
        headers = {}
    elif auth_correct:
        headers = {"Authorization": auth_token}
    else:
        token = "Basic " + base64.b64encode(f"bad_login:bad_password".encode()).decode()
        headers = {"Authorization": token}

    response = await test_client_rest.post(
        "/configs",
        params={
            "very_important_value": "new_value",
            "data_collection_time": "15:00:00",
        },
        headers=headers,
    )
    assert response.status_code == 200 if auth_correct else 401


@pytest.mark.asyncio
async def test_request_logging(
    dbsession: AsyncSession,
    test_client_rest: AsyncClient,
    auth_token,
):
    # clearing table to see only latest results
    logged_data_pre = await dbsession.execute(sa.delete(m.RequestLog))

    failed_request_data = {
        "very_important_value": "new_value",
        "data_collection_time": "14:00:00",
    }
    failed_response = await test_client_rest.post(
        "/configs",
        params=failed_request_data,
    )
    assert failed_response.status_code == 401

    successful_request_data = {
        "very_important_value": "new_value",
        "data_collection_time": "15:00:00",
    }
    successful_response = await test_client_rest.post(
        "/configs",
        params=successful_request_data,
        headers={"Authorization": auth_token},
    )
    assert successful_response.status_code == 200

    logged_data = (
        await dbsession.execute(
            sa.select(
                m.RequestLog.endpoint_address,
                m.RequestLog.response_code,
                m.RequestLog.request_data,
            )
        )
    ).fetchall()

    failed_logged_request = logged_data[0]
    assert failed_logged_request.endpoint_address == "/configs"
    assert failed_logged_request.response_code == 401
    assert failed_logged_request.request_data == failed_request_data

    successfull_logged_request = logged_data[1]
    assert successfull_logged_request.endpoint_address == "/configs"
    assert successfull_logged_request.response_code == 200
    assert successfull_logged_request.request_data == successful_request_data
