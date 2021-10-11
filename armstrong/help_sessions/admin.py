from django.contrib import admin
from django.forms import widgets, TextInput
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.safestring import mark_safe, SafeText, SafeData

from .models import Period, HelpSession


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ('user', lambda p: list(p.courses.all()), 'start_date', 'end_date', 'start_time', 'end_time',)
    list_filter =('user', 'courses', 'start_date', 'end_date',)


@admin.register(HelpSession)
class HelpSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'time', 'help_text', 'get_session_url',)
    list_filter =('date',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(teacher=request.user)

    @admin.display(description='SESSION URL')
    def get_session_url(self, h):
        return mark_safe('<a href="' + settings.URL + reverse('help_sessions:start', kwargs={'session_id': str(h.teacher.id) + '-' + str(h.user.id)}) + '" target="_blank">Open Session</a>')
