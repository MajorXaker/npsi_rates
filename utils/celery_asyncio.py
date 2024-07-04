from asyncio import sleep

from celery.result import AsyncResult

from config import log


async def celery_execute(func: callable, *args, **kwargs):
    """
    Executes a Celery task asynchronously.

    Args:
        func (callable): The Celery task function to be executed.
        *args: Positional arguments to be passed to the task function.
        **kwargs: Keyword arguments to be passed to the task function.

    Returns:
        The result of the Celery task if it is successful.

    Raises:
        Exception: If the Celery task is not successful. The exception message contains the task info.

    This function logs the execution of the Celery task and then waits for it to complete. It checks if the task is ready
    every second using an asynchronous sleep. If the task is successful, it returns the result. If the task is not
    successful, it raises an exception with the task info.
    """
    log.info(f"Executing celery task: {func.__name__}")
    task: AsyncResult = func.delay(*args, **kwargs)
    while not task.ready():
        await sleep(1)
    if task.successful():
        return task.result
    else:
        raise Exception(task.info)
