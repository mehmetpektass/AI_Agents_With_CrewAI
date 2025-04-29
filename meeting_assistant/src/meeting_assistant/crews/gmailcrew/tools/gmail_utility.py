from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.message import EmailMessage

import os
import base64
import markdown

SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]

HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
        {final_email_body}
    </body>
    </html>
"""


def gmail_authentication():
    """Shows basic usage of the Gmail API.
    Returns:
    service: Authorized Gmail API service instance.
    """

    current_dir = os.path.dirname(os.path.abspath(__file__))
    token_path = os.path.join(current_dir, "token.json")
    credential_path = os.path.join(current_dir, "credentials.json")

    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(credential_path):
                raise FileNotFoundError(
                    f"credentials.json not found at {credential_path}. "
                    "Please ensure you have downloaded your OAuth 2.0 credentials "
                    "from Google Cloud Console and placed them in the correct location."
                )

            flow = InstalledAppFlow.from_client_secrets_file(credential_path, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_path, "w") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)
    return service


def create_message(sender, to, subject, message_text):
    """Create a message for an email.

    Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email.
    message_text: The text of the email.

    Returns:
        An object containing a base64url encoded email object.
    """

    md = markdown.Markdown(extensions=["tables", "fenced_code", "nl2br"])

    formatted_html = HTML_TEMPLATE.format(final_email_body=md.convert(message_text))

    msg = EmailMessage()
    content = formatted_html

    msg["To"] = to
    msg["From"] = sender
    msg["Subject"] = subject
    msg.add_header("Content-Type", "text/html")
    msg.set_payload(content)

    encodeMsg = base64.urlsafe_b64encode(msg.as_bytes()).decode()

    return {"raw": encodeMsg}


def create_draft(service, user_id, message_body):
    """Create and insert a draft email.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
             can be used to indicate the authenticated user.
    message_body: The body of the draft email.

    R    eturns:
        The created draft.
    """

    try:
        draft = (
            service.users()
            .drafts()
            .create(userId=user_id, body={"message": message_body})
            .execute()
        )
        print(f'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')
        return draft
    except Exception as error:
        print(f"An error occurred: {error}")
        return None
