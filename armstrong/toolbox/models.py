from django.db import models

from course.models import Course


class ToolBox(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    courses = models.ManyToManyField(Course)

    def __str__(self):
        return f'{self.name}'
