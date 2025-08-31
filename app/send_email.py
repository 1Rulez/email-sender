import logging
import ssl
import aiosmtplib
import email.utils as utils

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.models import Email

logger = logging.getLogger("uvicorn")


async def email_sender(email: Email) -> None:
    msg = MIMEMultipart()
    msg["From"] = email.payload.from_field
    msg["Subject"] = email.payload.subject
    msg["To"] = ",".join(email.payload.to)
    msg['Message-ID'] = utils.make_msgid()
    msg['Date'] = utils.formatdate(localtime=True)
    context = ssl.create_default_context()
    if email.payload.to_copy:
        msg["Cc"] = ",".join(email.payload.to_copy)
    msg.attach(MIMEText(email.payload.content))
    async with aiosmtplib.SMTP(
            hostname=email.credentials.smtp_host,
            port=email.credentials.smtp_port,
            timeout=30,
            username=email.credentials.user,
            password=email.credentials.password,
            use_tls=True,
            tls_context=context
    ) as server:
        raw_response = await server.send_message(msg)
        logger.info(f"[INFO] From: {email.payload.from_field} To: {','.join(email.payload.to)}")
        logger.info(f"[INFO] Response: {raw_response}")
