"""authentication URL Configuration"""
from django.conf.urls import url

from authentication.views import LoginView, RegisterView


urlpatterns = [
    url(r'login/$', LoginView.as_view(), name='login'),
    url(r'register/$', RegisterView.as_view(), name='register')
]
