"""yola_auth URL Configuration. """
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include('users.urls', namespace='users')),
    url(r'^api/v1/', include('authentication.urls', namespace='auth')),
]
