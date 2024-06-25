import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from config import log
from models import db_models as m


async def update_step_in_db(session: AsyncSession, step: int):
    config_id = await session.scalar(sa.select(m.Config.id))

    if not config_id:
        raise Exception("Config not found")

    await session.execute(
        sa.update(m.Config).where(m.Config.id == config_id).values(step=step)
    )
    log.info(f"Step updated to {step}")
