from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework import permissions

from users.serializers import UserSerializer
from users.permissions import IsOwner


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)


