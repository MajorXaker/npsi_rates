import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from models import db_models as m
from datetime import datetime


async def save_rates(session: AsyncSession, rates: list[dict]):
    """
    Saves a list of rates to the database.

    Args:
        session (AsyncSession): The SQLAlchemy AsyncSession object.
        rates (list[dict]): A list of dictionaries representing the rates.

    Returns:
        None

    Raises:
        None
    """
    external_id_internal_id_mapping_q = sa.select(
        m.Currency.external_id, m.Currency.id
    ).where(m.Currency.external_id.in_([rate["Cur_ID"] for rate in rates]))

    external_id_internal_id_mapping = await session.execute(
        external_id_internal_id_mapping_q
    )

    external_id_internal_id_mapping = {
        external_id: internal_id
        for external_id, internal_id in external_id_internal_id_mapping.fetchall()
    }

    for rate in rates:
        currency_id = external_id_internal_id_mapping.get(rate["Cur_ID"])

        if not currency_id:
            insert_q = (
                sa.insert(m.Currency)
                .values(
                    external_id=rate["Cur_ID"],
                    abbreviation=rate["Cur_Abbreviation"],
                    name=rate["Cur_Name"],
                )
                .returning(m.Currency.id)
            )
            currency_id = await session.scalar(insert_q)
            external_id_internal_id_mapping[rate["Cur_ID"]] = currency_id

        insert_q = sa.insert(m.Rate).values(
            currency_id=currency_id,
            on_date=datetime.fromisoformat(rate["Date"]),
            scale=rate["Cur_Scale"],
            official_rate=rate["Cur_OfficialRate"],
        )

        await session.execute(insert_q)
