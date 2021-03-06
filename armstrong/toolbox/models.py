from django.db import models
from django.contrib.auth import get_user_model


class ToolBox(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    price_cents = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return f'{self.name}'

    def price_pounds(self):
        return round(self.price_cents/100, 2)


class Order(models.Model):
    bosta_id = models.CharField(max_length=255, null=False, blank=False)
    user = models.ForeignKey(get_user_model(), null=False, blank=False, on_delete=models.CASCADE, related_name='orders')
    toolbox = models.ForeignKey(ToolBox, null=False, blank=False, on_delete=models.CASCADE, related_name='orders')
