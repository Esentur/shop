# from django.core.mail import send_mail
#
#
# def send_confirmation_email(code, email):
#     full_link = f'http://localhost:8000/api/v1/account/activate/{code}'
#     send_mail(
#         'from shop project',  # topic
#         full_link,  # content
#         'esenturdildebekov8@gmail.com',  # from
#         [email]  # to
#     )
from django.core.mail import send_mail


def send_activation_email(code, email):
    full_link = f'http://localhost:8000/api/v1/account/activate/{code}'
    send_mail(
        'from SHOP PROJECT',
        full_link,
        'esenturdildebekov8@gmail.com',
        [email]
    )
