from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from .models import Student


@admin.register(get_user_model())
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    ordering = ('date_joined',)
    search_fields = ('first_name', 'last_name', 'email')
    list_display = ('email', 'is_confirmed', 'first_name',
                    'last_name', 'is_staff', 'membership',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')


@admin.register(Student)
class StudentAmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'birth_year',)
