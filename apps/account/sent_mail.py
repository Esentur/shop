from django.core.mail import send_mail


def send_confirmation_email(code, email):
    full_link = f'http://localhost:8000/api/v1/account/activate/{code}'
    send_mail(
        'from shop project',  # topic
        full_link,  # content
        'esenturdildebekov8@gmail.com',  # from
        [email]  # to
    )


def forgot_password_email(code, email):
    send_mail(
        'Восстановление пароля',
        f'Ваш код подтверждения: {code}',
        'esenturdildebekov8@gmail.com',
        [email]
    )

def send_order_confirmation(email,info):
    send_mail(
        ' Подтверждение покупки',
        f'Информация о покупке: {info}',
        'esenturdildebekov8@gmail.com',
        [email]
    )