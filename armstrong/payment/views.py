import json
import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth import get_user_model

from .forms import BillingDataForm
from .utils import AcceptAPI
from .models import Card, Invoice, Membership, CardToken


not_member_required = user_passes_test(lambda user: not user.is_member(), login_url='/')

@login_required
@not_member_required
def subscribe(request):
    context = {}
    if hasattr(request.user, 'billing_data'):
        context['billing_data'] = BillingDataForm(instance=request.user.billing_data)
    return render(template_name='masterstudy/subscribe.html', request=request, context=context)


@login_required
@not_member_required
def checkout(request):
    if hasattr(request.user, 'billing_data'):
        billing_data_form = BillingDataForm(request.POST, instance=request.user.billing_data)
    else:
        billing_data_form = BillingDataForm(request.POST)

    context = {
            'error': billing_data_form.errors,
            'billing_data': billing_data_form,
    }

    if not billing_data_form.is_valid():
        return render(template_name='masterstudy/subscribe.html', request=request, context=context)

    accept_api = AcceptAPI(settings.PAYMOB_API_KEY)

    auth_token = accept_api.retrieve_auth_token()

    order_data = {
        "auth_token": auth_token,
        "delivery_needed": "false",
        "amount_cents": "1100",
        "currency": "EGP",
        "items": [],
    }

    order = accept_api.order_registration(order_data)

    accept_api_request = {
        "auth_token": auth_token,
        "amount_cents": "1100",
        "expiration": 3600,
        "order_id": order.get("id"),
        "billing_data": {
            "apartment": "803",
            "email": "claudette09@exa.com",
            "floor": "42",
            "first_name": "Clifford",
            "street": "Ethan Land",
            "building": "8028",
            "phone_number": "+86(8)9135210487",
            "shipping_method": "PKG",
            "postal_code": "01898",
            "city": "Jaskolskiburgh",
            "country": "CR",
            "last_name": "Nicolas",
            "state": "Utah"
        },
        "currency": "EGP",
        "integration_id": 1139146,
        "lock_order_when_paid": "false"
    }

    payment_token = accept_api.payment_key_request(accept_api_request)

    iframe_url = accept_api.retrieve_iframe("4242", payment_token)

    context['iframe_url'] = iframe_url

    billing_data_form.save()

    return render(template_name='masterstudy/checkout.html', request=request, context=context)

@login_required
@not_member_required
def subscribe_done(request):
    context = {'billing_data': request.user.billing_data}
    t_data = request.GET

    if t_data['success'] == 'true':
        card, _ = Card.objects.update_or_create(
            user=request.user,
            defaults={
                'card_type': t_data['source_data.sub_type'],
                'last_4_digits': t_data['source_data.pan'],
            },
        )

        invoice, _ = Invoice.objects.update_or_create(
            user=request.user,
            defaults={
                'card': card,
                'paymob_id': t_data['id'],
                'service': 'Pro Membership',
                'billed': round(int(t_data['amount_cents'])/100, 2),
            }
        )

        membership, _ = Membership.objects.update_or_create(
            user=request.user,
            defaults={
                'status': Membership.ACTIVE,
                'activated_on': timezone.now(),
            }
        )

        context['card'] = card
        context['invoice'] = invoice

    context['message'] = t_data['data.message']

    return render(template_name='masterstudy/subscribe-done.html', request=request, context=context)

def save_token(request):
    req_data = json.dumps(request.body.decode('utf-8'))
    from django.core.mail import send_mail
    send_mail(
        subject='Armstrong Invoice',
        from_email=settings.FROM_EMAIL,
        recipient_list=['muhamedhassan8@icloud.com'],
        message=req_data,
        html_message=req_data,
    )
    if req_data['type'] == 'TOKEN':
        t_data = req_data['obj']

    CardToken.objects.update_or_create(
        user=get_user_model().objects.get(email=t_data['email'],
        defaults={
            'token': t_data['token'],
        }
    )
    return JsonResponse({}, status=204)
