from datetime import time

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models import db_models as m
import sqlalchemy as sa


@pytest.mark.asyncio
async def test_get_configs_empty(
    dbsession: AsyncSession, test_client_rest: AsyncClient, auth_token
):
    response = await test_client_rest.get(
        "/configs",
        headers={"Authorization": auth_token},
    )
    assert response.status_code == 200
    assert response.json() == {
        "very_important_value": None,
        "step": None,
        "data_collection_time": None,
    }


@pytest.mark.asyncio
async def test_get_configs_filled(
    dbsession: AsyncSession, test_client_rest: AsyncClient, auth_token
):

    await dbsession.execute(
        sa.insert(m.Config).values(
            very_important_value="test", step=1, data_collection_time=time(12, 0)
        )
    )

    response = await test_client_rest.get(
        "/configs", headers={"Authorization": auth_token}
    )
    assert response.status_code == 200
    assert response.json()["very_important_value"] == "test"
    assert response.json()["step"] == 1


@pytest.mark.asyncio
async def test_replace_configs(
    dbsession: AsyncSession,
    test_client_rest: AsyncClient,
    auth_token,
):
    response = await test_client_rest.post(
        "/configs",
        params={
            "very_important_value": "new_value",
            "data_collection_time": "14:00:00",
        },
        headers={"Authorization": auth_token},
    )
    assert response.status_code == 200
    configs = response.json()
    assert configs["very_important_value"] == "new_value"
    assert configs["data_collection_time"] == "14:00:00"

    # Verify the database update
    result = await dbsession.execute(select(m.Config))
    config = result.scalar_one()
    assert config.very_important_value == "new_value"
    assert str(config.data_collection_time) == "14:00:00"


@pytest.mark.asyncio
async def test_delete_configs(
    dbsession: AsyncSession, test_client_rest: AsyncClient, auth_token
):
    await dbsession.execute(
        sa.insert(m.Config).values(
            very_important_value="to_delete", data_collection_time=time(15, 0)
        )
    )

    response = await test_client_rest.delete(
        "/configs",
        headers={"Authorization": auth_token},
    )
    assert response.status_code == 200
    assert response.json() == {"Status": "OK"}

    result = await dbsession.scalar(select(m.Config.id))
    assert result is None


@pytest.mark.asyncio
async def test_update_configs(
    dbsession: AsyncSession, test_client_rest: AsyncClient, auth_token
):
    # Insert initial config
    await dbsession.execute(
        sa.insert(m.Config).values(
            very_important_value="original",
            data_collection_time=time(hour=16, minute=0, second=0),
            step=0,
        )
    )

    response = await test_client_rest.patch(
        "/configs",
        params={"very_important_value": "updated", "data_collection_time": "17:00:00"},
        headers={"Authorization": auth_token},
    )
    assert response.status_code == 200

    config = (
        await dbsession.execute(
            select(m.Config.very_important_value, m.Config.data_collection_time)
        )
    ).fetchone()

    assert config.very_important_value == "updated"
    assert str(config.data_collection_time) == "17:00:00"
