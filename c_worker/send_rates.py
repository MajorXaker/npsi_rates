from c_worker.celery import celery_worker
from config import log
from models import api_models as am
from utils.create_file_report import create_report_file
from utils.email_sender import email_handler


@celery_worker.task
def send_rates(recipients: list[str], rates: list[am.Rate]):
    try:
        attachment_data = create_report_file(rates)
        email_handler.send_email(
            recipients=recipients,
            subject="NBRB rates",
            email_text="Please see up-to-date rates attached to this email",
            attachment=attachment_data,
            attachment_name="rates.csv",
        )
    except Exception as e:
        log.error(e)
        return False
    else:
        return True
