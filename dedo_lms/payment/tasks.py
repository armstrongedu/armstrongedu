from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from dedo_lms.celery import app


@app.task
def test_task():
    send_mail(
        subject='test_task',
        from_email=settings.FROM_EMAIL,
        recipient_list=['hi@gaytomycode.com'],
        message='test',
        html_message='test',
    )
