import logging
import smtplib
import ssl
from email import encoders
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename
from typing import NoReturn

from retry import retry

from configuration import configs


class SendEmailFailure(Exception):
    """
    Raise email not sent
    """

    pass


server = None


def create_connection(from_email, from_email_password):
    global server
    sender_email = from_email
    if server:
        try:
            server.quit()
        except Exception:
            pass
        server = None
    context = ssl.create_default_context()
    if configs.MAIL_SERVER == "smtp.gmail.com":
        server = smtplib.SMTP_SSL(
            configs.MAIL_SERVER, configs.MAIL_PORT, context=context
        )
        server.login(sender_email, from_email_password)
    else:
        server = smtplib.SMTP(host=configs.MAIL_SERVER, port=configs.MAIL_PORT)
        server.starttls(context=context)
        server.login(sender_email, from_email_password)


def close_connection():
    global server
    if server:
        try:
            server.quit()
        except Exception:
            pass
        server = None


@retry(Exception, tries=3)
def send_email(recipient: str, subject: str, message: str, from_email: str, from_email_password: str) -> NoReturn:
    """
    Send email with okta credentials to recipient

    :param recipient:
    :param subject:
    :param message:
    :return:
    """

    global server
    if not server:
        create_connection(from_email, from_email_password)
    try:
        logging.info(f"Send email to {recipient} with subject {subject} and message:")

        receiver_email = recipient
        msg = message
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = from_email
        message["To"] = receiver_email
        part2 = MIMEText(msg, "html")
        message.attach(part2)
        server.sendmail(from_email, receiver_email, message.as_string())
    except Exception as ex:
        logging.error(str(ex))
        logging.error(f"Send email to {recipient} failure.")
        # Could be a connection error, retry!
        create_connection(from_email, from_email_password)
        raise SendEmailFailure


@retry(Exception, tries=3)
def send_pdf_email(recipient: str, subject: str, pdfs: list, from_email: str, from_email_password: str) -> NoReturn:
    """
    Send email with okta credentials to recipient

    :param recipient:
    :param subject:
    :param message:
    :return:
    """

    global server
    if not server:
        create_connection(from_email, from_email_password)
    try:
        logging.info(f"Send email to {recipient} with subject {subject} and message:")

        receiver_email = recipient
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = from_email
        message["To"] = receiver_email
        for each in pdfs:
            #
            # pdfname = each[1]
            # payload = MIMEBase('application', 'octet-stream', Name=pdfname)
            # payload.set_payload(each[0])
            # encoders.encode_base64(payload)
            # payload.add_header('Content-Disposition', 'attachment', filename=pdfname)
            # message.attach(payload)
            part = MIMEApplication(
                    each[0],
                    Name=each[1]
                )
            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(each[1])
            message.attach(part)

        #
        server.sendmail(from_email, receiver_email, message.as_string())
    except Exception as ex:
        logging.error(str(ex))
        logging.error(f"Send email to {recipient} failure.")
        # Could be a connection error, retry!
        create_connection(from_email, from_email_password)
        raise SendEmailFailure
