from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = settings.AUTH_USER_MODEL

class LoggedInUser(models.Model):
    user = models.OneToOneField(get_user_model(), null=False, blank=False, on_delete=models.CASCADE, related_name='login_sessions')
    session_key = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.email
