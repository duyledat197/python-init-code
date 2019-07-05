import os
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from celery_app import celery

CHARSET = "UTF-8"


def send_mail_reset_password(user, reset_link):
    path_file = 'template/mail-template/resetpassword.html'
    with open(path_file) as f:
        html = f.read()
    message = html.format(user=user, reset_link=reset_link)
    subject = 'Apac reset password'
    send_email.delay(user.email, subject, message)


def message_formatter(from_email, to_email, subject, message, images=None):
    if images is None:
        images = []
    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    msg_body = MIMEMultipart('alternative')
    html_part = MIMEText(message.encode(CHARSET), 'html', CHARSET)
    msg_body.attach(html_part)
    msg.attach(msg_body)

    for image in images:
        fp = open(image['path'], 'rb')
        msg_image = MIMEImage(fp.read())
        fp.close()
        msg_image.add_header('Content-ID', '<{cid}>'.format(cid=image['cid']))
        msg.attach(msg_image)

    return msg


@celery.task(name='tasks.mail.send_mail')
def send_email(to_email, subject, message, images=None):
    if images is None:
        images = []
    from_email = os.getenv("NO_REPLY_MAIL")
    s = smtplib.SMTP(os.getenv("AWS_SMTP_HOST"))
    try:
        s.connect(os.getenv("AWS_SMTP_HOST"), 587)
        s.starttls()
        s.login(os.getenv("AWS_SMTP_USERNAME"), os.getenv("AWS_SMTP_PASSWORD"))
        message = message_formatter(from_email, to_email, subject, message, images)
        s.sendmail(from_email, to_email, message.as_string())
        print("Email sent.")
    except Exception as e:
        print(e)
    finally:
        s.quit()
