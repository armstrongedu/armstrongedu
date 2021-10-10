from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.forms import widgets, TextInput
from django.db import models

from .models import Period, HelpSession


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ('user', lambda p: list(p.courses.all()), 'start_date', 'end_date', 'start_time', 'end_time',)
    list_filter =('user', 'courses', 'start_date', 'end_date',)


@admin.register(HelpSession)
class HelpSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'time', 'help_text',)
    list_filter =('date',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(teacher=request.user)
