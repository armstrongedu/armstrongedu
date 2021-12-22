from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings
from django.template.loader import render_to_string


def invoice_email(invoice):
    send_mail(
        subject='Armstrong Invoice',
        from_email=settings.FROM_EMAIL,
        recipient_list=[invoice.user.email],
        message=render_to_string('emails/invoice.html', {'user': invoice.user, 'billing_data': invoice.user.billing_data}),
        html_message=render_to_string('emails/invoice.html', {'user': invoice.user, 'billing_data': invoice.user.billing_data}),
        fail_silently=not settings.DEBUG,
    )
    send_mail(
        subject='Armstrong Invoice',
        from_email=settings.FROM_EMAIL,
        recipient_list=[invoice.user.email],
        message=render_to_string('emails/membership.html', {'user': invoice.user, 'billing_data': invoice.user.billing_data}),
        html_message=render_to_string('emails/membership.html', {'user': invoice.user, 'billing_data': invoice.user.billing_data}),
        fail_silently=not settings.DEBUG,
    )
