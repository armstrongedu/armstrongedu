from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test


from bostaSDK.apiClient import ApiClient
from bostaSDK import delivery
from bostaSDK import pickup
from bostaSDK.utils import Receiver, Address, ContactPerson, DeliveryTypes


from .models import Order
from payment.utils import AcceptAPI


member_required = user_passes_test(lambda user: user.is_member(), login_url='/')

@login_required
@member_required
def place_order(request):
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
