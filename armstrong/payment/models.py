from django.db import models
from django.contrib.auth import get_user_model


class MembershipType(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    price_cents = models.IntegerField(null=False, blank=False)
    number_of_students = models.IntegerField(null=False, blank=False)

    def price_pounds(self):
        return round(self.price_cents/100, 2)


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


class Invoice(models.Model):
    card = models.ForeignKey(Card, null=True, blank=True, on_delete=models.SET_NULL, related_name='invoices')
    paymob_id = models.CharField(max_length=255, null=False, blank=False)
    user = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL, related_name='invoices')
    created_at = models.DateTimeField(auto_now=True, null=False, blank=False)
    billed = models.FloatField(null=False, blank=False)

class CardToken(models.Model):
    user = models.OneToOneField(get_user_model(), null=False, blank=False, on_delete=models.CASCADE, related_name='card_token')
    token = models.CharField(max_length=255, null=False, blank=False)
