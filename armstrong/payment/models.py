from django.db import models
from django.contrib.auth import get_user_model

from . import utils


class MembershipType(models.Model):
    EGYPT = 'Egypt'
    QATAR = 'Qatar'
    BAHRAIN = 'Bahrain'
    SAUDI_ARABIA = 'Saudi Arabia'
    UNITED_ARAB_EMIRATES = 'United Arab Emirates'
    JORDAN = 'Jordan'
    KUWAIT = 'Kuwait'
    OMAN = 'Oman'
    INTERNATIONAL = 'International'

    STATUS = (
        (EGYPT, f'Egypt - {utils.CUR_EGYPT}'),
        (QATAR, f'Qatar - {utils.CUR_QATAR}'),
        (BAHRAIN, f'Bahrain - {utils.CUR_BAHRAIN}'),
        (SAUDI_ARABIA, f'Saudi Arabia {utils.CUR_SAUDI_ARABIA}'),
        (UNITED_ARAB_EMIRATES, f'United Arab Emiartes {utils.CUR_UNITED_ARAB_EMIRATES}'),
        (JORDAN, f'Jordan {utils.CUR_JORDAN}'),
        (KUWAIT, f'Kuwait {utils.CUR_KUWAIT}'),
        (OMAN, f'Oman {utils.CUR_OMAN}'),
        (INTERNATIONAL, f'International {utils.CUR_INTERNATIONAL}'),
    )

    country = models.CharField(max_length=255, choices=STATUS, null=False, blank=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    display_float_price = models.FloatField(null=False, blank=False)
    real_price_egyptian_cents = models.IntegerField(null=False, blank=False)
    number_of_students = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return f'{self.name} - {self.real_price_egyptian_cents} Egyptian Cents'

    def currency(self):
        return utils.CURRENCIES.get(self.country)


class BillingData(models.Model):
    user = models.OneToOneField(get_user_model(), null=False, blank=False, on_delete=models.CASCADE, related_name='billing_data')
    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    address_1 = models.CharField(max_length=255, null=False, blank=False)
    city = models.CharField(max_length=255, null=False, blank=False)
    state = models.CharField(max_length=255, null=False, blank=False)
    postal_code = models.CharField(max_length=255, null=False, blank=False)
    country = models.CharField(max_length=255, null=False, blank=False)
    phone = models.CharField(max_length=255, null=False, blank=False)
    email = models.CharField(max_length=255, null=False, blank=False)


class Membership(models.Model):
    ACTIVE, EXPIRED, CANCELED = range(1, 4)
    STATUS = (
        (ACTIVE, 'Active'),
        (EXPIRED, 'Expired'),
        (CANCELED, 'Canceled'),
    )

    user = models.OneToOneField(get_user_model(), null=False, blank=False, on_delete=models.CASCADE, related_name='membership')
    membership_type = models.ForeignKey(MembershipType, null=True, blank=True, on_delete=models.SET_NULL, related_name='memberships')
    activated_on = models.DateTimeField(null=False, blank=False)
    status = models.PositiveSmallIntegerField(choices=STATUS, null=False, blank=False, default=ACTIVE)

    def __str__(self):
        return f'{self.get_status_display()} - Started On: {self.activated_on.date()}'


class Card(models.Model):
    user = models.OneToOneField(get_user_model(), null=False, blank=False, on_delete=models.CASCADE, related_name='card')
    card_type = models.CharField(max_length=255, null=False, blank=False)
    last_4_digits = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.last_4_digits


class Invoice(models.Model):
    card = models.ForeignKey(Card, null=True, blank=True, on_delete=models.SET_NULL, related_name='invoices')
    paymob_id = models.CharField(max_length=255, null=False, blank=False)
    user = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL, related_name='invoices')
    item_name = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now=True, null=False, blank=False)
    item_price = models.FloatField(null=False, blank=False)
    promocode_price = models.FloatField(null=False, blank=False)
    billed = models.FloatField(null=False, blank=False)

class CardToken(models.Model):
    user = models.OneToOneField(get_user_model(), null=False, blank=False, on_delete=models.CASCADE, related_name='card_token')
    token = models.CharField(max_length=255, null=False, blank=False)


class Promocode(models.Model):
    promocode = models.CharField(max_length=255, null=False, blank=False)
    percent = models.IntegerField(null=False, blank=False)
