import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import render_template

def verification(receiver):
  try:
    verificationLink = f"http://127.0.0.1:7060/api/v1/user/verification?email={receiver}"
    sender = os.getenv('EMAIL_USERNAME')
    password = os.getenv('EMAIL_PASSWORD')
    subject = "Registration Email"
    message_html = f"<p>Click this <a href={verificationLink}>link</a> for verification your email.</p>"

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = "noreply@gmail.com"
    msg['To'] = receiver

    msg.attach(MIMEText(message_html, 'html'))

    server = smtplib.SMTP(os.getenv('EMAIL_HOST'), os.getenv('EMAIL_PORT'))
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, receiver, msg.as_string())

    print(f"Email was sent successfully to {receiver}")

    return "Success"

  except BaseException as e:
    print(e)
    return 'Fail'