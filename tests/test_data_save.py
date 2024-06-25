import pytest
import sqlalchemy as sa

from core.save_data import save_rates
from models import db_models as m


@pytest.mark.asyncio
async def test_data_save(dbsession):
    insert_usd_q = sa.insert(m.Currency).values(
        external_id=431,
        abbreviation="USD",
        name="Доллар США",
    )

    await dbsession.execute(insert_usd_q)

    sample_data = [
        {
            "Cur_Abbreviation": "EUR",
            "Cur_ID": 451,
            "Cur_Name": "Евро",
            "Cur_OfficialRate": 3.4496,
            "Cur_Scale": 1,
            "Date": "2024-06-24T00:00:00",
        },
        {
            "Cur_Abbreviation": "PLN",
            "Cur_ID": 452,
            "Cur_Name": "Злотых",
            "Cur_OfficialRate": 7.9613,
            "Cur_Scale": 10,
            "Date": "2024-06-24T00:00:00",
        },
        {
            "Cur_Abbreviation": "USD",
            "Cur_ID": 431,
            "Cur_Name": "Доллар США",
            "Cur_OfficialRate": 3.2257,
            "Cur_Scale": 1,
            "Date": "2024-06-24T00:00:00",
        },
        {
            "Cur_Abbreviation": "ISK",
            "Cur_ID": 453,
            "Cur_Name": "Исландских крон",
            "Cur_OfficialRate": 2.3138,
            "Cur_Scale": 100,
            "Date": "2024-06-24T00:00:00",
        },
        {
            "Cur_Abbreviation": "ISK",
            "Cur_ID": 453,
            "Cur_Name": "Исландских крон",
            "Cur_OfficialRate": 2.4,
            "Cur_Scale": 100,
            "Date": "2024-06-23T00:00:00",
        },
    ]

    await save_rates(dbsession, sample_data)

    rates_db = (await dbsession.scalars(sa.select(m.Rate.id))).fetchall()
    currencies_db = (await dbsession.scalars(sa.select(m.Currency.id))).fetchall()

    assert len(rates_db) == 5
    assert len(currencies_db) == 4
