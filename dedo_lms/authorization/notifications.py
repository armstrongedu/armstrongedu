from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings
from django.template.loader import render_to_string


def confirmation_email(user):
    send_mail(
        subject='Confirm Your Email',
        # from_email=settings.FROM_EMAIL,
        from_email='from@gmail.com',
        recipient_list=user.unconfirmed_emails,
        # message=render_to_string('emails/confirmation_code.html', {'user': user, 'settings': settings}),
        message='test',
        # html_message=render_to_string('emails/confirmation_code.html', {'user': user, 'settings': settings}),
        html_message='test',
        fail_silently=not settings.DEBUG,
    )
