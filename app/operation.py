
from fastapi import APIRouter
from app.models import Email
from app.send_email import email_sender

email_router = APIRouter(prefix="/email-sender", tags=["Отправка email"])


@email_router.post("/send-email")
async def send_email(email_data: Email):
    await email_sender(email_data)
