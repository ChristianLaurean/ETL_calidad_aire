import ssl
import smtplib
from config import EMAIL_PASSWORD
from email.message import EmailMessage
from constants import EMAIL_SENDER, EMAIL_RECIPIENT





def configure_email(subject: str, body: str) -> EmailMessage:
    """Configure the email message.

    Args:
        subject (str): The subject of the email.
        body (str): The body of the email.

    Returns:
        EmailMessage: An EmailMessage object configured with the specified subject and body.
    """
    message = EmailMessage()
    message["From"] = EMAIL_SENDER
    message["To"] = EMAIL_RECIPIENT
    message["Subject"] = subject
    message.set_content(body)
    return message




def send_email(message: EmailMessage) -> None:
    """Send the email message.

    Args:
        message (EmailMessage): The EmailMessage object to be sent.
    """
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, message.as_string())




def email_alert(subject: str, body: str) -> None:
    """Send an email with the specified subject and body.

    Args:
        subject (str): The subject of the email.
        body (str): The body of the email.
    """
    message = configure_email(subject, body)
    send_email(message)
