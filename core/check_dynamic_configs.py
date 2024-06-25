import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from models import api_models as am
from models import db_models as m


async def check_dynamic_configs(session: AsyncSession):
    dynamic_config = (
        await session.execute(
            sa.select(
                m.Config.very_important_value,
                m.Config.data_collection_time,
                m.Config.step,
            )
        )
    ).fetchone()
    if not dynamic_config:
        return None

    return am.Config.from_orm(dynamic_config)
