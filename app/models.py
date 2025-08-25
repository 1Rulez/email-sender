from typing import List

from pydantic import BaseModel, Field


class Credentials(BaseModel):
    smtp_host: str
    smtp_port: int
    user: str
    password: str
    tls: bool


class Payload(BaseModel):
    subject: str
    from_field: str = Field(alias='from')
    to: List[str]
    to_copy: List[str]
    content: str


class Email(BaseModel):
    credentials: Credentials
    payload: Payload
