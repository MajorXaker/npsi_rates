import sqlalchemy as sa
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session_dep
from models import api_models as am
from models import db_models as m
from models.api_models.rate import RatesResponse

rates_router = APIRouter()
# TODO Auth


@rates_router.get("/rates", tags=["rates"])
async def get_rates(
    db: AsyncSession = get_session_dep,
) -> RatesResponse:
    # TODO Return schema
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
    rates = [am.Rate.from_db_model(row) for row in data]
    return am.RatesResponse(rates=rates)
