from django.core.mail import send_mail

from apps.spam.models import Contact
from shop.celery import app


@app.task
def celery_email_about_product(product_info):
    for i in Contact.objects.all():
        send_mail(
            ' Новый товар это',
            f'{product_info}',
            'esenturdildebekov8@gmail.com',
            [i.email]
        )
