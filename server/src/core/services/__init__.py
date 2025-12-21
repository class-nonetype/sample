import os
import ssl
import smtplib
import asyncio
from typing import Sequence, Mapping, Any
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pydantic import EmailStr

from src.utils.properties import SMTP_SENDER, SMTP_SERVER, SMTP_PASSWORD, SMTP_PORT




def _build_message(
    to: Sequence[EmailStr],
    subject: str,
    body_html: str | None,
    body_text: str | None,
    headers: Mapping[str, Any] | None = None,
) -> MIMEMultipart | MIMEText:
    # Si hay HTML y texto plano, se manda multipart/alternative

    if body_html is not None and body_text is not None:
        msg = MIMEMultipart("alternative")
        msg.attach(MIMEText(body_text, "plain", "utf-8"))
        msg.attach(MIMEText(body_html, "html", "utf-8"))

    else:
        # HTML si existe, sino texto plano
        content = body_html if body_html is not None else (body_text or "")
        subtype = "html" if body_html is not None else "plain"
        msg = MIMEText(content, subtype, "utf-8")

    msg["Subject"] = subject
    msg["From"] = SMTP_SENDER
    msg["To"] = ",".join(str(x) for x in to)

    if headers:
        for key, value in headers.items():
            msg[key] = str(value)

    return msg


def _send_email_blocking(
    to: Sequence[EmailStr],
    subject: str,
    body_html: str | None,
    body_text: str | None,
    headers: Mapping[str, Any] | None = None,
) -> None:

    context = ssl.create_default_context()
    msg = _build_message(to, subject, body_html, body_text, headers)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(SMTP_SENDER, SMTP_PASSWORD)
        server.sendmail(SMTP_SENDER, [str(x) for x in to], msg.as_string())


async def send_email(
    to: Sequence[EmailStr],
    subject: str,
    body_html: str | None = None,
    body_text: str | None = None,
    headers: Mapping[str, Any] | None = None,
) -> None:

    loop = asyncio.get_running_loop()

    await loop.run_in_executor(
        None,
        _send_email_blocking,
        to,
        subject,
        body_html,
        body_text,
        headers,
    )
