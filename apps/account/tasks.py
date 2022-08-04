import time

from django.core.mail import send_mail

from shop.celery import app


@app.task
def celery_send_confirmation_email(code, email):
    time.sleep(10)
    full_link = f'http://localhost:8000/api/v1/account/activate/{code}'
    send_mail(
        'from shop project',  # topic
        full_link,  # content
        'esenturdildebekov8@gmail.com',  # from
        [email]  # to
    )

@app.task
def celery_send_order_confirmation(email,info):
    time.sleep(15)
    send_mail(
        ' Подтверждение покупки',
        f'Информация о покупке: {info}',
        'esenturdildebekov8@gmail.com',
        [email]
    )

@app.task
def celery_spam_email():
    # time.sleep(15)
    spam_text='Hello spam from Account'
    send_mail(
        ' Спам сообщение',
        f'{spam_text}',
        'esenturdildebekov8@gmail.com',
        ['esenturdildebekov8@gmail.com']
    )

@app.task
def send_info_about_activation(email):
    send_mail(
        'Вы активировали аккаунт!',
        'Можете залогиниться!',
        'esenturdildebekov8@gmail.com',
        [email]
    )