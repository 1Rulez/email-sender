import smtplib
import logging

import aiosmtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.models import Email

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


async def send_email(email: Email):
    msg = MIMEMultipart()
    msg["From"] = email.payload.from_field
    msg["Subject"] = email.payload.subject
    msg["To"] = ",".join(email.payload.to)
    msg["Cc"] = ",".join(email.payload.to_copy)

    msg.attach(MIMEText(email.payload.content))

    server = smtplib.SMTP(email.credentials.smtp_host)
    server.connect(
        email.credentials.smtp_host,
        email.credentials.smtp_port
    )

    if email.credentials.tls:
        logger.debug("TLS started")
        server.starttls()

    logger.debug(msg.as_string())

    server.login(email.credentials.user, email.credentials.password)
    server.sendmail(
        email.credentials.user,
        email.payload.to + email.payload.to_copy,
        msg.as_string()
    )
    server.quit()


async def email_sender(email: Email) -> None:
    msg = MIMEMultipart()
    msg["From"] = email.payload.from_field
    msg["Subject"] = email.payload.subject
    msg["To"] = ",".join(email.payload.to)
    if email.payload.to_copy:
        msg["Cc"] = ",".join(email.payload.to_copy)
    msg.attach(MIMEText(email.payload.content))

    async with aiosmtplib.SMTP(
            hostname=email.credentials.smtp_host,
            port=email.credentials.smtp_port,
            timeout=30,
            username=email.credentials.user,
            password=email.credentials.password,
    ) as server:
        raw_response = await server.send_message(msg, timeout=30)
        logger.debug(f"[INFO] Response: {raw_response}")
