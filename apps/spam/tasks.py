from django.core.mail import send_mail

from apps.spam.models import Contact
from shop.celery import app


@app.task
def celery_spam_todo():
    # time.sleep(15)
    for i in Contact.objects.all():
        spam_text='Hello spam from Spam'
        send_mail(
            ' Спам сообщение',
            f'{spam_text}',
            'esenturdildebekov8@gmail.com',
            [i.email]
        )