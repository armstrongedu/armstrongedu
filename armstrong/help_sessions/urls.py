from django.urls import path

from . import views


urlpatterns = [
    path('place-help', views.place_help, name='place-help'),
]
