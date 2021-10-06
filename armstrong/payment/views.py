import json
import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

from .forms import BillingDataForm
from .utils import AcceptAPI
from .models import Card, Receipt, Membership, CardToken, MembershipType


not_member_required = user_passes_test(lambda user: not user.is_member(), login_url='/')

@login_required
@not_member_required
def subscribe(request):
    context = {'membership_types': MembershipType.objects.all()}
    if hasattr(request.user, 'billing_data'):
        context['billing_data'] = BillingDataForm(instance=request.user.billing_data)
    return render(template_name='masterstudy/subscribe.html', request=request, context=context)


@login_required
@not_member_required
def checkout(request):
    membership_type = MembershipType.objects.get(id=request.POST['membership_type'])

    if hasattr(request.user, 'billing_data'):
        billing_data_form = BillingDataForm(request.POST, instance=request.user.billing_data)
    else:
        billing_data_form = BillingDataForm(request.POST)


    context = {
            'membership_types': MembershipType.objects.all(),
            'membership_type': membership_type,
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
        "amount_cents": membership_type.price_cents,
        "currency": "EGP",
        "items": [{
            "name": membership_type.name,
            "amount_cents": membership_type.price_cents,
            "description": membership_type.name,
            "quantity": 1,
        },],
    }

    order = accept_api.order_registration(order_data)

    accept_api_request = {
        "auth_token": auth_token,
        "amount_cents": membership_type.price_cents,
        "expiration": 3600,
        "order_id": order.get("id"),
        "billing_data": {
            "apartment": billing_data_form['address_1'].value(),
            "email": request.user.email,
            "floor": "-",
            "first_name": billing_data_form['first_name'].value(),
            "street": "-",
            "building": "-",
            "phone_number": billing_data_form['phone'].value(),
            "shipping_method": "-",
            "postal_code": billing_data_form['postal_code'].value(),
            "city": billing_data_form['city'].value(),
            "country": billing_data_form['country'].value(),
            "last_name": billing_data_form['last_name'].value(),
            "state": billing_data_form['state'].value(),
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
    # TODO: here i should do the toolbox order
    context = {'billing_data': request.user.billing_data}
    t_data = request.GET

    if t_data['success'] == 'true':

        accept_api = AcceptAPI(settings.PAYMOB_API_KEY)
        item_name = json.loads(accept_api.retrieve_transaction(t_data['id']))['obj']['order']['items'][0]['name']

        membership_type = MembershipType.objects.filter(name=name)
        context['membership_type'] = membership_type

        card, _ = Card.objects.update_or_create(
            user=request.user,
            defaults={
                'card_type': t_data['source_data.sub_type'],
                'last_4_digits': t_data['source_data.pan'],
            },
        )

        invoice, _ = Receipt.objects.update_or_create(
            user=request.user,
            defaults={
                'card': card,
                'paymob_id': t_data['id'],
                'billed': round(int(t_data['amount_cents'])/100, 2),
            }
        )

        membership, _ = Membership.objects.update_or_create(
            user=request.user,
            defaults={
                'status': Membership.ACTIVE,
                'membership_type': membership_type,
                'activated_on': timezone.now(),
            }
        )

        context['card'] = card
        context['invoice'] = invoice

    context['message'] = t_data['data.message']

    return render(template_name='masterstudy/subscribe-done.html', request=request, context=context)

@csrf_exempt
def save_token(request):
    req_data = json.loads(request.body.decode('utf-8'))
    if req_data['type'] == 'TOKEN':
        t_data = req_data['obj']

        CardToken.objects.update_or_create(
            user=get_user_model().objects.get(email=t_data['email']),
            defaults={
                'token': t_data['token'],
            }
        )
    return JsonResponse({}, status=204)
