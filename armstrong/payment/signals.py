from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from . import notifications
from .models import Receipt


@receiver(post_save, sender=Receipt)
def new_receipt_added(sender, instance, **kwargs):
    notifications.receipt_email(instance)
