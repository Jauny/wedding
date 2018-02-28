# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import logging
import os
import sendgrid
from app import config
from sendgrid.helpers.mail import Mail, Email, Content  # noqa

logger = logging.getLogger(__name__)
sg = sendgrid.SendGridAPIClient(apikey=config.get('SENDGRID_API_KEY'))

FROM_EMAIL = 'jypepin@gmail.com'


def send_email(to_email, subject, html_body):
    """Send email to to_email, with subject and body."""
    logger.info({'msg': 'sending email', 'to_email': to_email, 'subject': subject})

    mail = Mail(
      Email(FROM_EMAIL),
      subject,
      Email(to_email),
      Content("text/plain", html_body))

    response = sg.client.mail.send.post(request_body=mail.get())

    logger.info('sent email', to_email=to_email, subject=subject)


def send_invite_email(to_emails):
    """Send invite to email."""
    logger.info({'msg': 'sending invite email', 'to_emails': to_emails})

    personalizations = [{
      'to': [{'email': to_email}],
      'substitutions': {
        ':base_url': 'http://wpwedding.herokuapp.com',
        ':to_email': to_email
      }
    } for to_email in to_emails]

    data = {
      'personalizations': personalizations,
      'from': {
        'email': 'hello@jonathanandjessicawedding.com',
        'name': 'Jonathan and Jessica'
      },
      'template_id': 'd4297acf-b9cd-4f62-a971-a774ba69adaa',
      'tracking_settings': {
        'click_tracking': {
          'enable': True
        }
      }
    }

    response = sg.client.mail.send.post(request_body=data)
    logger.info({'msg': 'sent invite emails', 'response': response})



# from_email = Email("test@example.com")
# to_email = Email("test@example.com")
# subject = "Sending with SendGrid is Fun"
# content = Content("text/plain", "and easy to do anywhere, even with Python")
# mail = Mail(from_email, subject, to_email, content)
# response = sg.client.mail.send.post(request_body=mail.get())
# print(response.status_code)
# print(response.body)
# print(response.headers)
