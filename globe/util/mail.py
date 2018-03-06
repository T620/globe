from flask_mail import Message

from globe import mail


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender[0], recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)
