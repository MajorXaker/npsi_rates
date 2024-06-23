import sqlalchemy as sa
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from db import get_session_dep
from models import db_models as m
from models import api_models as am

rates_router = APIRouter()
# TODO Auth


@rates_router.get("/rates", tags=["healthcheck"])
async def get_rates(
    db: AsyncSession = get_session_dep,
):
    # TODO Pagination
    data = (
        await db.execute(
            sa.select(
                m.Currency.abbreviation,
                m.Currency.name,
                m.Currency.external_id,
                m.Rate.official_rate,
                m.Rate.on_date,
                m.Rate.scale,
            ).select_from(
                sa.join(m.Rate, m.Currency, m.Rate.currency_id == m.Currency.id)
            )
        )
    ).fetchall()
    rates = [am.Rate.from_db_model(**row._asdict()).model_dump_json() for row in data]
    return JSONResponse({"rates": rates}, status.HTTP_200_OK)
