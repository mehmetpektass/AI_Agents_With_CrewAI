import os

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

    cred = None
    
     