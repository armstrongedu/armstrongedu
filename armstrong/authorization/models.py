from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin
from django.utils.timezone import now

from .managers import UserManager


class User(SimpleEmailConfirmationUserMixin, AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def is_member(self):
        from payment.models import Membership
        return hasattr(self, 'membership') and (self.membership.status == Membership.ACTIVE)

    def has_students(self):
        return self.membership.membership_type.number_of_students == self.students.count()

    def is_free_trial(self):
        return not self.is_member() and (now() - self.date_joined).days <= 14

    def is_plus(self):
        return self.is_member() and self.membership.membership_type.plan == self.membership.membership_type.PLUS


class Student(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE, related_name='students')
    name = models.CharField(max_length=255, null=False, blank=False)
    birth_year = models.IntegerField(null=False, blank=False)


class Newsletter(models.Model):
    email = models.CharField(max_length=255, null=False, blank=False)
