from celery import Celery
from db import RABBITMQ_CONNECTION_URL

celery_worker = Celery(
    "nbrb_rates_worker",
    broker=RABBITMQ_CONNECTION_URL,
    backend="rpc://",
    include=["c_worker.fetch_data_nbrb"],
)

# Optional configuration, see the application user guide.
celery_worker.conf.update(
    result_expires=7200,
)

if __name__ == "__main__":
    celery_worker.start()
