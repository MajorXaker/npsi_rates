from asyncio import sleep

from celery.result import AsyncResult

from config import log


async def celery_execute(func: callable, *args, **kwargs):
    log.info(f"Executing celery task: {func.__name__}")
    task: AsyncResult = func.delay(args=args, kwargs=kwargs)
    while not task.ready():
        await sleep(1)
    if task.successful():
        return task.result
    else:
        raise Exception(task.info)
