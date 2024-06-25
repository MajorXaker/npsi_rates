import pytest
from freezegun import freeze_time

from core.check_dynamic_configs import check_dynamic_configs
from core.scheduling import get_data_collection_time, time_left_for_collection
from models import db_models as m
import sqlalchemy as sa
from models import api_models as am
from datetime import time, datetime, timedelta


@pytest.mark.asyncio
async def test_get_time(dbsession):
    config_insert_q = sa.insert(m.Config).values(
        {
            m.Config.very_important_value: "important value",
            m.Config.step: 1,
            m.Config.data_collection_time: time(hour=12, minute=0, second=0),
        }
    )

    await dbsession.execute(config_insert_q)

    time_to_collect_data = await get_data_collection_time(dbsession)

    frozen_time = datetime(2024, 1, 1, 11, 48, 0)
    with freeze_time(frozen_time):
        time_left = await time_left_for_collection(time_to_collect_data)
        assert time_left == timedelta(seconds=720)

    frozen_time = datetime(2024, 1, 1, 11, 56, 0)
    with freeze_time(frozen_time):
        time_left = await time_left_for_collection(time_to_collect_data)
        assert time_left == timedelta(seconds=240)


@pytest.mark.asyncio
async def test_get_configs(dbsession):
    config_insert_q = sa.insert(m.Config).values(
        {
            m.Config.very_important_value: "important value",
            m.Config.step: 1,
            m.Config.data_collection_time: time(hour=12, minute=0, second=0),
        }
    )

    await dbsession.execute(config_insert_q)

    configs = await check_dynamic_configs(dbsession)

    assert configs == am.Config(
        very_important_value="important value",
        step=1,
        data_collection_time=time(hour=12, minute=0, second=0),
    )
