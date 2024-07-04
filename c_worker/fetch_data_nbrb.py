import httpx

from c_worker.celery import celery_worker


async def get_currencies():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.nbrb.by/exrates/currencies")
        response.raise_for_status()
        return response.json()


@celery_worker.task
def get_rates(*args, **kwargs):
    """
    Retrieves the exchange rates from the National Bank of the Republic of Belarus API.

    This function sends an HTTP GET request to the "https://api.nbrb.by/exrates/rates" URL with the "periodicity" parameter set to 0.
    It expects the API to return a JSON response containing the exchange rates.

    Returns:
        dict: A dictionary representing the exchange rates. The keys are the currency codes and the values are the exchange rates.

    Raises:
        httpx.HTTPStatusError: If the API returns a non-successful status code.

    """
    response = httpx.get("https://api.nbrb.by/exrates/rates", params={"periodicity": 0})
    response.raise_for_status()
    return response.json()
