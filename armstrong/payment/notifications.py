from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings
from django.template.loader import render_to_string


def receipt_email(receipt):
    send_mail(
        subject='Armstrong Receipt',
        from_email=settings.FROM_EMAIL,
        recipient_list=[receipt.user.email],
        # message=render_to_string('emails/confirmation_code.html', {'user': user, 'settings': settings}),
        message='Receipt',
        # html_message=render_to_string('emails/confirmation_code.html', {'user': user, 'settings': settings}),
        html_message='Receipt',
        fail_silently=not settings.DEBUG,
    )
