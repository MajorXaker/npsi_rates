from datetime import datetime, time, timedelta

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from models import db_models as m


async def get_data_collection_time(session: AsyncSession) -> sa.Time:
    data_collection_time = await session.scalar(
        sa.select(m.Config.data_collection_time)
    )
    return data_collection_time


async def time_left_for_collection(scheduled_time: datetime.time):
    current_time = datetime.utcnow()
    current_timedelta = timedelta(
        seconds=current_time.second,
        minutes=current_time.minute,
        hours=current_time.hour,
    )

    scheduled_timedelta = timedelta(
        seconds=scheduled_time.second,
        minutes=scheduled_time.minute,
        hours=scheduled_time.hour,
    )

    return scheduled_timedelta - current_timedelta
