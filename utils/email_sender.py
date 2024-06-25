import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import settings as s, log


class EmailHandler:
    username: str
    password: str
    smtp_server: str
    port: int
    email_disabled: bool

    def __init__(
        self,
    ):
        """
        Initializes the EmailHandler object.

        Parameters:
            self: The EmailHandler object itself.

        Returns:
            None
        """
        if not any(
            [
                s.SMTP_SERVER,
                s.SMTP_PORT,
                s.SMTP_LOGIN,
                s.SMTP_PASSWORD,
            ]
        ):
            self.email_disabled = True
        else:
            self.email_disabled = False

        self.smtp_server = s.SMTP_SERVER
        self.port = s.SMTP_PORT
        self.username = s.SMTP_LOGIN
        self.password = s.SMTP_PASSWORD

        self.use_ssl = s.USE_SSL

    def _prepare_email(
        self,
        recipients: list[str],
        subject: str,
        email_text: str = None,
        attachment=None,
        attachment_name: str = "data.csv",
    ):
        if self.email_disabled:
            log.info("Email sending is disabled")
            return None, None

        msg = MIMEMultipart()
        msg["From"] = self.username
        msg["To"] = ", ".join(recipients)
        msg["Subject"] = subject
        msg.attach(MIMEText(email_text, "plain"))

        if attachment:
            part = MIMEBase("application", "octet-stream")
            in_memory_csv_bytes = attachment.getvalue().encode("utf-8")
            part.set_payload(in_memory_csv_bytes)
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition", f"attachment; filename= {attachment_name}"
            )
            msg.attach(part)
        text = msg.as_string()

        return msg, text

    def _send(self, message, text):
        if self.email_disabled:
            log.info("Email sending is disabled")
            return

        if self.use_ssl:
            server_func = smtplib.SMTP_SSL
        else:
            server_func = smtplib.SMTP

        with server_func(self.smtp_server, self.port) as smtp_server:
            smtp_server.login(self.username, self.password)
            smtp_server.sendmail(message["From"], message["To"].split(","), text)

    def send_email(
        self,
        recipients: list[str],
        subject: str,
        email_text: str = None,
        attachment=None,
        attachment_name: str = "data.csv",
    ):
        """
        Sends an email to the specified recipients with the given subject and optional email text and attachment.

        Parameters:
            recipients (list[str]): List of email addresses to send the email to.
            subject (str): Subject of the email.
            email_text (str, optional): Main text content of the email. Defaults to None.
            attachment (optional): Attachment file to be sent. Defaults to None.
            attachment_name (str, optional): Name of the attachment file. Defaults to "data.csv".
        """
        try:
            msg, text = self._prepare_email(
                recipients=recipients,
                subject=subject,
                email_text=email_text,
                attachment=attachment,
                attachment_name=attachment_name,
            )

            self._send(message=msg, text=text)

        except Exception as e:
            log.exception(e)
            log.info("Email was not sent, exception occurred")
        else:
            log.info(f"Email was sent successfully to {len(recipients)} recipients")


email_handler = EmailHandler()
