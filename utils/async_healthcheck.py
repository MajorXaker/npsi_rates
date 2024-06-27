import asyncio
from pathlib import Path

from config import settings


async def healthcheck():
    """
    This function runs indefinitely and continuously touches the file specified by `CORE_ALIVE_FILE_PATH` every 30 seconds. The file is created if it does not exist, and its last modification time is updated otherwise.
    This file is being checked by healthcheck_probe.py.

    This function does not take any parameters.

    This function does not return any value.

    Raises:
        None
    """
    if settings.CORE_ALIVE_FILE_PATH:
        while True:
            Path(settings.CORE_ALIVE_FILE_PATH).touch()
            await asyncio.sleep(30)
