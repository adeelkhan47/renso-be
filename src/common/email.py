import logging
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import NoReturn

from retry import retry

from conf import settings


class SendEmailFailure(Exception):
    """
    Raise email not sent
    """

    pass


server = None


def create_connection():
    global server
    sender_email = settings.MAIL_USERNAME
    if server:
        try:
            server.quit()
        except Exception:
            pass
        server = None
    context = ssl.create_default_context()
    if settings.MAIL_SERVER == "smtp.gmail.com":
        server = smtplib.SMTP_SSL(
            settings.MAIL_SERVER, settings.MAIL_PORT, context=context
        )
        server.login(sender_email, settings.MAIL_PASSWORD)
    else:
        server = smtplib.SMTP(host=settings.MAIL_SERVER, port=settings.MAIL_PORT)
        server.starttls(context=context)
        server.login(sender_email, settings.MAIL_PASSWORD)


def close_connection():
    global server
    if server:
        try:
            server.quit()
        except Exception:
            pass
        server = None


@retry(Exception, tries=3)
def send_email(recipient: str, subject: str, message: str) -> NoReturn:
    """
    Send email with okta credentials to recipient

    :param recipient:
    :param subject:
    :param message:
    :return:
    """

    try:
        logging.info(f"Send email to {recipient} with subject {subject} and message:")
        sender_email = settings.MAIL_USERNAME
        receiver_email = recipient
        msg = message
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = receiver_email
        part2 = MIMEText(msg, "html")
        message.attach(part2)
        server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as ex:
        logging.error(str(ex))
        logging.error(f"Send email to {recipient} failure.")
        # Could be a connection error, retry!
        create_connection()
        raise SendEmailFailure
