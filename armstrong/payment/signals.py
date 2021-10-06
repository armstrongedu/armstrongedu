from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from . import notifications
from .models import Invoice


@receiver(post_save, sender=Invoice)
def new_invoice_added(sender, instance, **kwargs):
    notifications.invoice_email(instance)
