# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os

import sendgrid
from sendgrid.helpers.mail import *

import pdb; pdb.set_trace();

sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
from_email = Email("test@example.com")
to_email = Email("test@example.com")
subject = "Sending with SendGrid is Fun"
content = Content("text/plain", "and easy to do anywhere, even with Python")
mail = Mail(from_email, subject, to_email, content)
response = sg.client.mail.send.post(request_body=mail.get())
print(response.status_code)
print(response.body)
print(response.headers)