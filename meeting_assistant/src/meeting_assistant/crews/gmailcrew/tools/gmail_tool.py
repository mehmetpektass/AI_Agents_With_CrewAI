from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from .gmail_utility import gmail_authentication, create_message, create_draft
import os


class GmailToolInput(BaseModel):
    """Input schema for MyCustomTool."""

    body: str = Field(..., description="The body of the email to sent.")


class GmailTool(BaseTool):
    name: str = "GmailTool"
    description: str = "Tool for sending emails through Gmail."
    args_schema: Type[BaseModel] = GmailToolInput

    def _run(self, body: str | dict) -> str:

        if isinstance(body, dict):
            body = body.get("description", body.get("content", str(body)))

        try:
            service = gmail_authentication()
            sender = os.getenv("GMAIL_SENDER")
            to = os.getenv("GMAIL_RECIPIENT")
            subject = "Meeting Minutes"
            message_text = str(body)

            message = create_message(sender, to, subject, message_text)
            draft = create_draft(service, "me", message)

            return f"Email sent successfully! Draft id: {draft['id']}"
        except Exception as e:
            return f"Error sending email: {e}"
