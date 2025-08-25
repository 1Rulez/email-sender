import logging

from fastapi import APIRouter, HTTPException
from app.models import Email
from app.send_email import email_sender


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

email_router = APIRouter()


@email_router.post("/send-email")
async def post_call_result(email_data: Email):
    try:
        await email_sender(email_data)
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))
