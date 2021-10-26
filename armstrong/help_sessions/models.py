from django.db import models
from django.contrib.auth import get_user_model

from course.models import Course


class Period(models.Model):
    user = models.ForeignKey(get_user_model(), null=False, blank=False, on_delete=models.CASCADE, related_name='help_period')
    courses = models.ManyToManyField(Course, related_name='periods')
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    start_time = models.TimeField(null=False, blank=False)
    end_time = models.TimeField(null=False, blank=False)


class HelpSession(models.Model):
    user = models.ForeignKey(get_user_model(), null=False, blank=False, on_delete=models.CASCADE, related_name='help_sessions')
    teacher = models.ForeignKey(get_user_model(), null=False, blank=False, on_delete=models.CASCADE, related_name='teacher_help_sessions')
    date = models.DateField(null=False, blank=False)
    time = models.TimeField(null=False, blank=False)
    help_text = models.CharField(max_length=255, null=True, blank=True)
