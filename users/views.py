from django.contrib.auth import get_user_model

from rest_framework import viewsets, mixins
from rest_framework import permissions

from users.serializers import UserSerializer
from users.permissions import IsOwnerOrReadOnly


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)


