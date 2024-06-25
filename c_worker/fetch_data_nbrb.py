import httpx

from c_worker.celery import celery_worker


async def get_currencies():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.nbrb.by/exrates/currencies")
        response.raise_for_status()
        return response.json()


@celery_worker.task
def get_rates():
    response = httpx.get("https://api.nbrb.by/exrates/rates", params={"periodicity": 0})
    response.raise_for_status()
    return response.json()
