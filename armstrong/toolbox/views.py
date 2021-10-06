from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test


from bostaSDK.apiClient import ApiClient
from bostaSDK import delivery
from bostaSDK import pickup
from bostaSDK.utils import Receiver, Address, ContactPerson, DeliveryTypes

from payment.models import Receipt

from .models import Order, Toolbox
from payment.utils import AcceptAPI


member_required = user_passes_test(lambda user: user.is_member(), login_url='/')

@login_required
@member_required
def place_order(request):
    toolbox = Toolbox.objects.get(id=request.POST['tool_box_id'])
    billing_data = request.user.billing_data

    accept_api = AcceptAPI(settings.PAYMOB_API_KEY)

    auth_token = accept_api.retrieve_auth_token()

    order_data = {
        "auth_token": auth_token,
        "delivery_needed": "false",
        "amount_cents": toolbox.price_cents,
        "currency": "EGP",
        "items": [{
            "name": toolbox.name,
            "amount_cents": toolbox.price_cents,
            "description": toolbox.name,
            "quantity": 1,
        },],
    }


    order = accept_api.order_registration(order_data)

    accept_api_request = {
        "auth_token": auth_token,
        "amount_cents": toolbox.price_cents,
        "expiration": 3600,
        "order_id": order.get("id"),
        "billing_data": {
            "apartment": billing_data.address_1,
            "email": request.user.email,
            "floor": "-",
            "first_name": billing_data.first_name,
            "street": "-",
            "building": "-",
            "phone_number": billing_data.phone,
            "shipping_method": "-",
            "postal_code": billing_data.postal_code,
            "city": billing_data.city,
            "country": billing_data.country,
            "last_name": billing_data.last_name,
            "state": billing_data.state,
        },
        "currency": "EGP",
        "integration_id": 1139146,
        "lock_order_when_paid": "false"
    }

    payment_token = accept_api.payment_key_request(accept_api_request)

    payment_resp = accept_api.pay(request.user.card_token.token, 'TOKEN', payment_token)

    if payment_resp['obj']['success'] == 'true':
        receipt = Receipt.objects.create(
            user = request.user,
            card = request.user.card,
            paymob_id = payment_resp['obj']['id'],
            billed = round(int(payment_resp['obj']['amount_cents'])/100, 2),
        )
        api_client=ApiClient(settings.BOSTA_API_KEY)

        delivery_types = api_client.deliveyTypes

        billing_data = request.user.billing_data
        reciever = Receiver(billing_data.first_name, billing_data.last_name, billing_data.email, billing_data.phone)
        drop_off_address = Address(billing_data.city, billing_data.address_1, district=billing_data.state, zone=billing_data.city)

        delivery_req = delivery.create.CreateDeliveryRequest(
            delivery_types['SEND']['code'],
            0, drop_off_address, reciever
        )
        delivery_resp = api_client.delivery.create(delivery_req)
        bosta_id = delivery_resp.get_deliveryId()

        Order.objects.create(bosta_id=bosta_id, user=request.user, toolbox_id=request.POST['tool_box_id'])

        contact_person = ContactPerson(settings.BOSTA_USERNAME, settings.BOSTA_NUMBER, settings.BOSTA_EMAIL)
        pickup_req = pickup.create.CreatePickupRequest(
            (datetime.now()+timedelta(1)).strftime('%a %b %d %Y 10:00:00 GMT+0200'),
            api_client.pickupTimeSlots[0], contact_person
        )
        pickup_resp = api_client.pickup.create(pickup_req)

    return redirect('main:home')
