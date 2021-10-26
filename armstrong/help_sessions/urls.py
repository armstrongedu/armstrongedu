from django.urls import path

from . import views


urlpatterns = [
    path('place-help', views.place_help, name='place-help'),
    path('start/<str:session_id>', views.start_help, name='start'),
]
