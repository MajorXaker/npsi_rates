from datetime import date

import pytest
import sqlalchemy as sa
from models import db_models as m


@pytest.mark.asyncio
async def test_api_rates(test_client_rest, creator, dbsession):
    currency_id = await creator.create_currency(abbreviation="USD")

    await creator.create_rates(
        currency_id,
        date(2022, 1, 1),
        date(2022, 1, 20),
    )

    rates_db = (await dbsession.execute(sa.select(m.Rate.__table__.c))).fetchall()

    rates_from_api = (await test_client_rest.get("/rates")).json()

    assert len(rates_from_api["rates"]) == len(rates_db)
