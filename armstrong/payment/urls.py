from django.urls import path

from . import views

urlpatterns = [
    path('subscribe/', views.subscribe, name='subscribe'),
    path('checkout/', views.checkout,  name='checkout'),
    path('subscribe-done/', views.subscribe_done,  name='subscribe-done'),
    path('upgrade/', views.upgrade, name='upgrade'),
    path('upgrade-checkout/', views.upgrade_checkout,  name='upgrade-checkout'),
    path('save-token/', views.save_token, name='save-token'),
]
