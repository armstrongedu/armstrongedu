from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from dedo_lms.celery import app


@app.task
def test_task(email_list):
    from urllib.request import urlopen
    import json
    resp = json.loads(urlopen('http://ron-swanson-quotes.herokuapp.com/v2/quotes').read())[0]
    message = '''<p>Morning,</p>
    <p>How was sleep fighting? Did you know that ''' + resp + '''.</p>
<p>Sincerely,</p>
<p>Ron Swanson</p>'''
    send_mail(
        subject='Ron Swanson',
        from_email=settings.FROM_EMAIL,
        recipient_list=email_list,
        message=message,
        html_message=message,
    )
