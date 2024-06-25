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
    current_time = datetime.utcnow().time()
    current_seconds = (
        current_time.hour * 3600 + current_time.minute * 60 + current_time.second
    )
    scheduled_seconds = (
        scheduled_time.hour * 3600 + scheduled_time.minute * 60 + scheduled_time.second
    )
    time_left = scheduled_seconds - current_seconds
    return time(
        hour=time_left // 3600,
        minute=(time_left % 3600) // 60,
        second=(time_left % 3600) % 60,
    )
