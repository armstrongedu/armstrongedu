from django.db import models
from django.contrib.auth import get_user_model


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


class Invoice(models.Model):
    ...

class Membership(models.Model):
    ACTIVE, EXPIRED, CANCELED = range(1, 4)
    STATUS = (
        (ACTIVE, 'Active'),
        (EXPIRED, 'Expired'),
        (CANCELED, 'Canceled'),
    )

    user = models.OneToOneField(get_user_model(), null=False, blank=False, on_delete=models.CASCADE, related_name='membership')
    activated_on = models.DateTimeField(auto_now=True, null=False, blank=False)
    status = models.PositiveSmallIntegerField(choices=STATUS, null=False, blank=False, default=ACTIVE)

    def __str__(self):
        return f'{self.get_status_display()} - Started On: {self.activated_on.date()}'
