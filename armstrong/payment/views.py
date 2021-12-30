import json
import datetime
import re

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.contrib.gis.geoip2 import GeoIP2


from .forms import BillingDataForm
from .utils import AcceptAPI
from .models import Card, Invoice, Membership, CardToken, MembershipType, Promocode


not_member_required = user_passes_test(lambda user: not user.is_member(), login_url='/')
member_required = user_passes_test(lambda user: user.is_member(), login_url='/')

@login_required
@not_member_required
def subscribe(request):
    g = GeoIP2()
    client_ip = request.META.get('REMOTE_ADDR') or request.META.get('HTTP_X_FORWARDED_FOR')
    try:
        country = g.country(client_ip).get('country_name')
    except Exception:
        localized_membership_type = MembershipType.objects.filter(country=MembershipType.INTERNATIONAL)
    else:
        localized_membership_type = MembershipType.objects.filter(country=country)
        if not localized_membership_type.exists():
            localized_membership_type = MembershipType.objects.filter(country=MembershipType.INTERNATIONAL)
    context = {'membership_types': localized_membership_type}
    if hasattr(request.user, 'billing_data'):
        context['billing_data'] = BillingDataForm(instance=request.user.billing_data)
    return render(template_name=f'masterstudy/subscribe{"_ar" if settings.AS_LANG == "ar" else ""}.html', request=request, context=context)


@login_required
@not_member_required
def checkout(request):
    membership_type = MembershipType.objects.get(id=request.POST['membership_type'])
    promocode = promocode_post = request.POST.get('promocode')
    num_of_stds = request.POST.get('number_of_students')
    if promocode_post:
        promocode = Promocode.objects.filter(promocode=promocode_post)


    if hasattr(request.user, 'billing_data'):
        billing_data_form = BillingDataForm(request.POST, instance=request.user.billing_data)
    else:
        billing_data_form = BillingDataForm(request.POST)


    g = GeoIP2()
    client_ip = request.META.get('REMOTE_ADDR') or request.META.get('HTTP_X_FORWARDED_FOR')
    try:
        country = g.country(client_ip).get('country_name')
    except Exception:
        localized_membership_type = MembershipType.objects.filter(country=MembershipType.INTERNATIONAL)
    else:
        localized_membership_type = MembershipType.objects.filter(country=country)
        if not localized_membership_type.exists():
            localized_membership_type = MembershipType.objects.filter(country=MembershipType.INTERNATIONAL)
    context = {
            'membership_types': localized_membership_type,
            'membership_type': membership_type,
            'error': billing_data_form.errors,
            'billing_data': billing_data_form,
    }

    if promocode_post and not promocode.exists():
        context['error'] = 'Promocode Not Valid!'
        return render(template_name=f'masterstudy/subscribe{"_ar" if settings.AS_LANG == "ar" else ""}.html', request=request, context=context)

    if not num_of_stds or not num_of_stds.isdigit() or int(num_of_stds)-1 < 0:
        context['error'] = 'Number of Students Not Valid!'
        return render(template_name=f'masterstudy/subscribe{"_ar" if settings.AS_LANG == "ar" else ""}.html', request=request, context=context)
    num_of_stds = int(num_of_stds) - 1

    if promocode_post:
        promocode = promocode.first()
        promocode_price = int(membership_type.real_price_egyptian_cents * promocode.percent // 100)
        promocode_display = int(membership_type.display_float_price * promocode.percent // 100)
    else:
        promocode_price = 0
        promocode_display = 0.0

    if num_of_stds:
        num_of_stds_price = int(membership_type.std_real_price_egyptian_cents * int(num_of_stds))
        num_of_stds_display = int(membership_type.std_display_float_price * int(num_of_stds))
    else:
        num_of_stds_price = 0
        num_of_stds_display = 0.0

    if not billing_data_form.is_valid():
        return render(template_name=f'masterstudy/subscribe{"_ar" if settings.AS_LANG == "ar" else ""}.html', request=request, context=context)

    accept_api = AcceptAPI(settings.PAYMOB_API_KEY)

    auth_token = accept_api.retrieve_auth_token()

    order_data = {
        "auth_token": auth_token,
        "delivery_needed": "false",
        "amount_cents": membership_type.real_price_egyptian_cents - promocode_price + num_of_stds_price,
        "currency": "EGP",
        "items": [{
            "name": membership_type.id,
            "amount_cents": membership_type.real_price_egyptian_cents,
            "description": membership_type.name,
            "quantity": 1,
        }, {
            "name": 'PROMOCODE',
            "amount_cents": promocode_price,
            "description": promocode.promocode if promocode_post else '',
            "quantity": 1,
        },{
            "name": 'STDS',
            "amount_cents": num_of_stds_price,
            "description": str(num_of_stds),
            "quantity": int(num_of_stds),
        }],
    }

    order = accept_api.order_registration(order_data)

    accept_api_request = {
        "auth_token": auth_token,
        "amount_cents": membership_type.real_price_egyptian_cents - promocode_price + num_of_stds_price,
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
        "integration_id": settings.PAYMOB_PAYMENT_ID,
        "lock_order_when_paid": "false"
    }

    payment_token = accept_api.payment_key_request(accept_api_request)

    iframe_url = accept_api.retrieve_iframe("4242", payment_token)

    context['iframe_url'] = iframe_url
    if promocode_post:
        context['promocode'] = promocode
    context['num_of_stds'] = num_of_stds
    context['promocode_display'] = round(int(promocode_display), 2)
    context['num_of_stds_display'] = round(int(num_of_stds_display), 2)
    context['net_price'] = round(int(membership_type.display_float_price - promocode_display + num_of_stds_display), 2)


    billing_data_form.save()

    return render(template_name=f'masterstudy/checkout{"_ar" if settings.AS_LANG == "ar" else ""}.html', request=request, context=context)

@login_required
def subscribe_done(request):
    context = {'billing_data': request.user.billing_data}
    t_data = request.GET

    if t_data['success'] == 'true':

        accept_api = AcceptAPI(settings.PAYMOB_API_KEY)
        items = accept_api.retrieve_transaction(t_data['id'])['order']['items']
        if len(items) > 1:
            for item in items:
                if item['name'] == 'PROMOCODE':
                    promocode_price = item['amount_cents']
                    promocode_name = item['description']
                elif item['name'] == 'STDS':
                    num_of_stds_price = item['amount_cents']
                    num_of_stds = int(item['description'])
                else:
                    item_name = item['name']
                    item_price = item['amount_cents']
                    item_description = item['description']
        else:
            item_name = items[0]['name']
            item_description = items[0]['description']

        membership_type = MembershipType.objects.get(id=item_name)
        context['membership_type'] = membership_type

        card, _ = Card.objects.update_or_create(
            user=request.user,
            defaults={
                'card_type': t_data['source_data.sub_type'],
                'last_4_digits': t_data['source_data.pan'],
            },
        )

        g = GeoIP2()
        client_ip = request.META.get('REMOTE_ADDR') or request.META.get('HTTP_X_FORWARDED_FOR')
        try:
            country = g.country(client_ip).get('country_name')
        except Exception:
            country = MembershipType.INTERNATIONAL
        if hasattr(request.user, 'membership') and request.user.membership.status == Membership.ACTIVE:
            old_membership = request.user.membership
            old_membership_type = request.user.membership.membership_type
            was_billed = (old_membership_type.real_price_egyptian_cents + old_membership_type.std_real_price_egyptian_cents  * (old_membership.number_of_students-1))
            credit_left = round((was_billed *  (30-int((timezone.now() - old_membership.activated_on).days))/30 ) / 100, 2)
            context['credit_left'] = credit_left
            billed = round(int(t_data['amount_cents'])/100 - credit_left, 2)
        else:
            billed = round(int(t_data['amount_cents'])/100, 2)
        invoice = Invoice.objects.create(
            user = request.user,
            card = card,
            country = country,
            paymob_id = t_data['id'],
            item_name = item_description,
            promocode_name = promocode_name,
            item_price = round(int(item_price)/100, 2),
            promocode_price = round(int(promocode_price)/100, 2),
            add_stds_price = round(int(num_of_stds_price)/100, 2),
            billed = billed,
        )

        membership, _ = Membership.objects.update_or_create(
            user=request.user,
            defaults={
                'status': Membership.ACTIVE,
                'membership_type': membership_type,
                'activated_on': timezone.now(),
                'number_of_students': num_of_stds + 1,
            }
        )
        # request.user.students.all().delete()

        context['card'] = card
        context['invoice'] = invoice

    context['message'] = t_data['data.message']

    return render(template_name=f'masterstudy/subscribe-done{_ar if settings.AS_LANG == "ar" else ""}.html', request=request, context=context)

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


@login_required
@member_required
def upgrade(request):
    g = GeoIP2()
    client_ip = request.META.get('REMOTE_ADDR') or request.META.get('HTTP_X_FORWARDED_FOR')
    try:
        country = g.country(client_ip).get('country_name')
    except Exception:
        localized_membership_type = MembershipType.objects.filter(country=MembershipType.INTERNATIONAL)
    else:
        localized_membership_type = MembershipType.objects.filter(country=country)
        if not localized_membership_type.exists():
            localized_membership_type = MembershipType.objects.filter(country=MembershipType.INTERNATIONAL)
    context = {'membership_types': localized_membership_type}
    if hasattr(request.user, 'billing_data'):
        context['billing_data'] = BillingDataForm(instance=request.user.billing_data)
    return render(template_name=f'masterstudy/upgrade{"_ar" if settings.AS_LANG == "ar" else ""}.html', request=request, context=context)


@login_required
@member_required
def upgrade_checkout(request):
    membership_type = MembershipType.objects.get(id=request.POST['membership_type'])
    promocode = promocode_post = request.POST.get('promocode')
    num_of_stds = request.POST.get('number_of_students')
    if promocode_post:
        promocode = Promocode.objects.filter(promocode=promocode_post)


    if hasattr(request.user, 'billing_data'):
        billing_data_form = BillingDataForm(request.POST, instance=request.user.billing_data)
    else:
        billing_data_form = BillingDataForm(request.POST)


    g = GeoIP2()
    client_ip = request.META.get('REMOTE_ADDR') or request.META.get('HTTP_X_FORWARDED_FOR')
    try:
        country = g.country(client_ip).get('country_name')
    except Exception:
        localized_membership_type = MembershipType.objects.filter(country=MembershipType.INTERNATIONAL)
    else:
        localized_membership_type = MembershipType.objects.filter(country=country)
        if not localized_membership_type.exists():
            localized_membership_type = MembershipType.objects.filter(country=MembershipType.INTERNATIONAL)
    context = {
            'membership_types': localized_membership_type,
            'membership_type': membership_type,
            'error': billing_data_form.errors,
            'billing_data': billing_data_form,
    }

    if promocode_post and not promocode.exists():
        context['error'] = 'Promocode Not Valid!'
        return render(template_name=f'masterstudy/upgrade{"_ar" if settings.AS_LANG == "ar" else ""}.html', request=request, context=context)

    if not num_of_stds or not num_of_stds.isdigit() or int(num_of_stds)-1 < 0:
        context['error'] = 'Number of Students Not Valid!'
        return render(template_name=f'masterstudy/upgrade{"_ar" if settings.AS_LANG == "ar" else ""}.html', request=request, context=context)
    num_of_stds = int(num_of_stds) - 1

    if promocode_post:
        promocode = promocode.first()
        promocode_price = int(membership_type.real_price_egyptian_cents * promocode.percent // 100)
        promocode_display = int(membership_type.display_float_price * promocode.percent // 100)
    else:
        promocode_price = 0
        promocode_display = 0.0

    if num_of_stds:
        num_of_stds_price = int(membership_type.std_real_price_egyptian_cents * int(num_of_stds))
        num_of_stds_display = int(membership_type.std_display_float_price * int(num_of_stds))
    else:
        num_of_stds_price = 0
        num_of_stds_display = 0.0

    if not billing_data_form.is_valid():
        return render(template_name=f'masterstudy/upgrade{"_ar" if settings.AS_LANG == "ar" else ""}.html', request=request, context=context)

    accept_api = AcceptAPI(settings.PAYMOB_API_KEY)

    auth_token = accept_api.retrieve_auth_token()

    order_data = {
        "auth_token": auth_token,
        "delivery_needed": "false",
        "amount_cents": membership_type.real_price_egyptian_cents - promocode_price + num_of_stds_price,
        "currency": "EGP",
        "items": [{
            "name": membership_type.id,
            "amount_cents": membership_type.real_price_egyptian_cents,
            "description": membership_type.name,
            "quantity": 1,
        }, {
            "name": 'PROMOCODE',
            "amount_cents": promocode_price,
            "description": promocode.promocode if promocode_post else '',
            "quantity": 1,
        },{
            "name": 'STDS',
            "amount_cents": num_of_stds_price,
            "description": str(num_of_stds),
            "quantity": int(num_of_stds),
        }],
    }

    order = accept_api.order_registration(order_data)

    accept_api_request = {
        "auth_token": auth_token,
        "amount_cents": membership_type.real_price_egyptian_cents - promocode_price + num_of_stds_price,
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
        "integration_id": settings.PAYMOB_PAYMENT_ID,
        "lock_order_when_paid": "false"
    }

    payment_token = accept_api.payment_key_request(accept_api_request)

    iframe_url = accept_api.retrieve_iframe("4242", payment_token)

    context['iframe_url'] = iframe_url
    if promocode_post:
        context['promocode'] = promocode
    old_membership = request.user.membership
    old_membership_type = request.user.membership.membership_type
    billed = (old_membership_type.display_float_price + old_membership_type.std_display_float_price  * (old_membership.number_of_students-1))
    credit_left = billed *  (30-int((timezone.now() - old_membership.activated_on).days))/30
    context['credit_left'] = round(int(credit_left), 2)
    context['num_of_stds'] = num_of_stds
    context['promocode_display'] = round(int(promocode_display), 2)
    context['num_of_stds_display'] = round(int(num_of_stds_display), 2)
    context['net_price'] = round(int(membership_type.display_float_price - promocode_display + num_of_stds_display - int(credit_left)), 2)


    billing_data_form.save()

    return render(template_name=f'masterstudy/upgrade-checkout{"_ar" if settings.AS_LANG == "ar" else ""}.html', request=request, context=context)
