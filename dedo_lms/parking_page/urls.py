from django.urls import path

from . import views


urlpatterns = [
    path('', views.parking_page, name='parking_page'),
]
