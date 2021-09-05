from django.urls import path

from . import views

urlpatterns = [
    path('', views.courses, name='courses'),
    path('<course_id>', views.course, name='course'),
]
