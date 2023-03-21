from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic import EmailStr

from src.config.manager import settings


class EmailService:
    def __init__(self, username: str, url: str, emails: list[EmailStr]):
        self.username = username
        self.sender = settings.MAIL_FROM
        self.emails = emails
        self.url = url
        pass

    async def send_email(self, subject: str, template_name: str):
        conf = ConnectionConfig(
            MAIL_USERNAME=settings.MAIL_USERNAME,
            MAIL_PASSWORD=settings.MAIL_PASSWORD,
            MAIL_FROM=self.sender,
            MAIL_FROM_NAME=settings.MAIL_FROM_USERNAME,
            MAIL_PORT=settings.MAIL_PORT,
            MAIL_SERVER=settings.MAIL_SERVER,
            MAIL_STARTTLS=settings.IS_STARTTLS,
            MAIL_SSL_TLS=settings.IS_SSL_TLS,
            USE_CREDENTIALS=settings.IS_USE_CREDENTIALS,
            MAIL_DEBUG=1,
            TEMPLATE_FOLDER=settings.TEMPLATE_DIR,
        )

        env = Environment(
            loader=FileSystemLoader(searchpath=settings.TEMPLATE_DIR), autoescape=select_autoescape(["html", "xml"])
        )
        template = env.get_template(name=f"{template_name}.html")
        html = template.render(url=self.url, username=self.username, subject=subject)

        await FastMail(conf).send_message(
            message=MessageSchema(subject=subject, recipients=self.emails, body=html, subtype=MessageType.html),
            template_name=f"{template_name}.html",
        )

    async def send_account_verification(self):
        await self.send_email(subject="Pala Blog - Email Confirmation", template_name="verification")
