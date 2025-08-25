import uvicorn

from fastapi import FastAPI
from app.operation import email_router


def create_application():
    app = FastAPI(
        title="API отправки сообщений на почту",
        summary="Служба отправки сообщений на почту",
    )
    app.include_router(email_router)

    return app


uvicorn.run(app=create_application(), host="0.0.0.0")
