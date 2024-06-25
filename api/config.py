from datetime import time

import sqlalchemy as sa
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from db import get_session_dep
from models import db_models as m

config_router = APIRouter()
# TODO Auth


@config_router.get("/configs", tags=["configs"])
async def get_configs(
    db: AsyncSession = get_session_dep,
):
    data = (
        await db.execute(
            sa.select(
                m.Config.very_important_value,
                m.Config.step,
                m.Config.data_collection_time,
            )
        )
    ).fetchone()

    data = (
        data._asdict()
        if data
        else {"very_important_value": None, "step": None, "data_collection_time": None}
    )
    return JSONResponse({"configs": data}, status.HTTP_200_OK)


@config_router.post("/configs", tags=["configs"])
async def replace_configs(
    very_important_value: str,
    data_collection_time: time,
    db: AsyncSession = get_session_dep,
):
    # Config entry should be the only one, so we delete it first
    await db.execute(sa.delete(m.Config))

    data = (
        await db.execute(
            sa.insert(m.Config).values(
                {
                    m.Config.very_important_value: very_important_value,
                    m.Config.step: 0,
                    m.Config.data_collection_time: data_collection_time,
                }
            )
        )
    ).fetchone()
    return JSONResponse({"configs": data._asdict()}, status.HTTP_200_OK)


@config_router.delete("/configs", tags=["configs"])
async def delete_configs(
    db: AsyncSession = get_session_dep,
):
    await db.execute(sa.delete(m.Config))
    return JSONResponse({"Status": "OK"}, status.HTTP_200_OK)


@config_router.patch("/configs", tags=["configs"])
async def update_configs(
    very_important_value: str = None,
    data_collection_time: time = None,
    db: AsyncSession = get_session_dep,
):
    config_id = await db.scalar(sa.select(m.Config.id))

    update_q = (
        sa.update(m.Config)
        .where(m.Config.id == config_id)
        .returning(
            m.Config.very_important_value,
            m.Config.data_collection_time,
        )
    )
    if very_important_value:
        update_q = update_q.values(very_important_value=very_important_value)
    if data_collection_time:
        update_q = update_q.values(data_collection_time=data_collection_time)
    config_data = (await db.execute(update_q)).fetchone()

    return JSONResponse({"Config": config_data._asdict()}, status.HTTP_200_OK)
