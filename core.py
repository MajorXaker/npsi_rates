import asyncio
from datetime import timedelta

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from c_worker.fetch_data_nbrb import get_rates
from c_worker.send_rates import send_rates
from config import settings as s, log
from core.check_dynamic_configs import check_dynamic_configs
from core.save_data import save_rates
from core.scheduling import get_data_collection_time, time_left_for_collection
from db import persistent_engine
from models import db_models as m
from utils.async_healthcheck import healthcheck
from utils.celery_asyncio import celery_execute
from utils.step_handler import update_step_in_db


async def main():
    """
    The main function of the CORE module. It runs an infinite loop that checks for dynamic configurations,
    performs data collection and email sending based on the step value in the configurations,
    and handles exceptions. The function uses celery to perform asynchronous tasks.

    Parameters:
    None

    Returns:
    None
    """
    log.info("Core module started")
    while True:
        healthcheck_task = asyncio.create_task(healthcheck())
        try:
            async with AsyncSession(persistent_engine) as session, session.begin():
                configs = await check_dynamic_configs(session)
            if not configs:
                log.info(
                    f"No configs available. Core module sleeping {s.NO_CONFIG_IDLE_TIME}"
                )
                await asyncio.sleep(s.NO_CONFIG_IDLE_TIME)
                continue

            async with AsyncSession(persistent_engine) as session, session.begin():
                time_to_collect_data = await get_data_collection_time(session)
                time_left = await time_left_for_collection(time_to_collect_data)
            if configs.step == 4 and time_left.days == -1:
                log.info("Data has been already collected today. Sleeping")
                await asyncio.sleep(60)
                continue
            elif configs.step == 4 and time_left < timedelta(3600):
                async with AsyncSession(persistent_engine) as session, session.begin():
                    await update_step_in_db(session, 0)
            elif configs.step == 0 and time_left < timedelta(60):
                async with AsyncSession(persistent_engine) as session, session.begin():
                    await update_step_in_db(session, 1)
                    nbrb_rates = await celery_execute(get_rates)
                    await update_step_in_db(session, 2)

                    await save_rates(session, nbrb_rates)
                    log.info("Data saved")
                    await update_step_in_db(session, 3)

                    recipients = (
                        await session.scalars(sa.select(m.EmailRecipient.email))
                    ).fetchall()
                    log.info(f"Sending emails to {len(recipients)} recipients")

                    is_ok = await celery_execute(
                        send_rates, recipients=recipients, rates=nbrb_rates
                    )
                    if is_ok:
                        log.info(f"Emails sent to {len(recipients)} recipients")
                    await update_step_in_db(session, 4)

            else:
                log.info(
                    "Time to collect data is not reached. Core module sleeping 60 seconds"
                )
                await asyncio.sleep(60)

        except Exception as exp:
            log.exception(exp)
            await asyncio.sleep(60)
        healthcheck_task.cancel()

    log.info("Core module shutting down")


if __name__ == "__main__":
    asyncio.run(main())
