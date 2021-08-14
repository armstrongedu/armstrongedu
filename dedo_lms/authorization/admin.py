from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model


@admin.register(get_user_model())
class UserAdmin(UserAdmin):
    ordering = ('date_joined',)
    list_display = ('email', 'is_confirmed', 'first_name',
                    'last_name', 'is_staff', 'confirmed_emails',
                    'unconfirmed_emails')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')


