import random
from datetime import date, timedelta

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from models import db_models as m


class Creator:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_currency(
        self,
        abbreviation: str,
        name: str = None,
    ):
        if not name:
            name = f"Currency_{abbreviation}"

        available_id = (
            await self.session.scalar(sa.select(sa.func.max(m.Currency.external_id)))
            or 0
        )
        available_id += 1

        currency_id = await self.session.scalar(
            sa.insert(m.Currency)
            .values(
                {
                    m.Currency.abbreviation: abbreviation,
                    m.Currency.name: name,
                    m.Currency.external_id: available_id,
                }
            )
            .returning(m.Currency.id)
        )
        return currency_id

    async def create_rates(
        self,
        currency_id: int,
        start_date: date,
        end_date: date = None,
    ):
        if not end_date:
            end_date = start_date + timedelta(days=1)

        days = [
            start_date + timedelta(days=i) for i in range((end_date - start_date).days)
        ]

        rates = []
        for rate_date in days:
            rates.append(
                dict(
                    currency_id=currency_id,
                    on_date=rate_date,
                    scale=random.randint(1, 10),
                    official_rate=random.randint(1, 1000) / 100,
                )
            )

        await self.session.execute(sa.insert(m.Rate).values(rates))
