from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('cert/<cert_id>', views.cert, name='cert'),
]
