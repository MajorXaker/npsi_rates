import base64

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


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

    response = await test_client_rest.get("/configs", headers=headers)
    assert response.status_code == 200 if auth_correct else 401

    response = await test_client_rest.get(
        "/configs",
        headers={"Authorization": auth_token},
    )
    assert response.status_code == 200 if auth_correct else 401
