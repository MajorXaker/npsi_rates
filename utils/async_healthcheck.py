import asyncio
from pathlib import Path

from config import settings


async def healthcheck():
    if settings.MS_ALIVE_FILE_PATH:
        while True:
            Path(settings.MS_ALIVE_FILE_PATH).touch()
            await asyncio.sleep(30)
