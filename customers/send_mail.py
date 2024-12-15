from django.core.mail import send_mail

from R4C import settings


def send_email(email, model, version):

    subject = 'Ваш робот дожидается вас!'

    message = f"""Добрый день!
Недавно вы интересовались нашим роботом модели {model}, версии {version}.
Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами."""

    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [email])