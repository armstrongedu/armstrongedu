from django.urls import path

from . import views

urlpatterns = [
    path('subscribe/', views.subscribe, name='subscribe'),
    path('checkout/', views.checkout,  name='checkout'),
    path('subscribe-done/', views.subscribe_done,  name='subscribe-done'),
]
