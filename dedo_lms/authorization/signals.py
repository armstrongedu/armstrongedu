from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from . import notifications


@receiver(post_save, sender=get_user_model())
def new_user_added(sender, instance, **kwargs):
    if not instance.is_confirmed:
        notifications.confirmation_email(instance)
