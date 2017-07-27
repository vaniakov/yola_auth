from django.contrib.auth.models import User

from rest_framework import viewsets, mixins
from rest_framework import permissions

from users.serializers import UserSerializer
from users.permissions import IsOwnerOrReadOnly


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)


