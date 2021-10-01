from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings
from django.template.loader import render_to_string


def invoice_email(invoice):
    send_mail(
        subject='Armstrong Invoice',
        from_email=settings.FROM_EMAIL,
        recipient_list=[invoice.user.email],
        # message=render_to_string('emails/confirmation_code.html', {'user': user, 'settings': settings}),
        message='INVOCIE',
        # html_message=render_to_string('emails/confirmation_code.html', {'user': user, 'settings': settings}),
        html_message='INVOCIE',
        fail_silently=not settings.DEBUG,
    )
