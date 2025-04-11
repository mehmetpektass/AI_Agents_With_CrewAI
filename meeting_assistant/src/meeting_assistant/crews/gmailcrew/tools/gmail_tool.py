from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from gmail_utility import gmail_authentication, create_message, create_draft

import os

class GmailToolInput(BaseModel):
    """Input schema for MyCustomTool."""

    argument: str = Field(..., description="Description of the argument.")


class GmailTool(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, body: str) -> str:
        try:
            service = gmail_authentication()
            sender = os.getenv("GMAIL_SENDER")
            to = os.getenv("GMAIL_RECIPIENT")
            subject = "Meeting Minutes"
            message_text = body

            message = create_message(sender, to, subject, message_text)
            draft = create_draft(service, "me", message)

            return f"Email sent successfully! Draft id: {draft['id']}"
        except Exception as e:
            return f"Error sending email: {e}"
