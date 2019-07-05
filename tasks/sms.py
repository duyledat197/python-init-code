import os

from twilio.rest import Client

from celery_app import celery


@celery.task(name='tasks.mail.send_sms')
def send_sms(to_phone_number, message):
    client = Client(
        os.getenv('TWILIO_ACCOUNT_ID'),
        os.getenv('TWILIO_AUTH_TOKEN'),

    )
    message = client.messages.create(
        body=message,
        to=to_phone_number,
        from_='ROCKSHIP'
    )

# if __name__ == '__main__':
#     send_sms(
#         '+6584298483',
#         'this is test message'
#     )
