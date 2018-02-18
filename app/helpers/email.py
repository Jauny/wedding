# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
from app import config, logger
import sendgrid
from sendgrid.helpers.mail import *

sg = sendgrid.SendGridAPIClient(apikey=config.get('SENDGRID_API_KEY'))

FROM_EMAIL = 'jypepin@gmail.com'

def send_email(to_email, subject, html_body):
    """Send email to to_email, with subject and body."""
    logger.info('sending email', to_email=to_email, subject=subject)

    mail = Mail(
      Email(FROM_EMAIL),
      subject,
      Email(to_email),
      Content("text/plain", html_body))

    response = sg.client.mail.send.post(request_body=mail.get())

    logger.info('sent email', to_email=to_email, subject=subject)

# from_email = Email("test@example.com")
# to_email = Email("test@example.com")
# subject = "Sending with SendGrid is Fun"
# content = Content("text/plain", "and easy to do anywhere, even with Python")
# mail = Mail(from_email, subject, to_email, content)
# response = sg.client.mail.send.post(request_body=mail.get())
# print(response.status_code)
# print(response.body)
# print(response.headers)