from django.contrib.auth import (
    login as django_login,
)

from rest_framework import status
from rest_framework import views, generics
from rest_framework import permissions
from rest_framework.response import Response

from authentication.serializers import LoginSerializer
from authentication.serializers import TokenSerializer
from authentication.serializers import RegisterSerializer
from rest_framework.authtoken.models import Token


class LoginView(generics.GenericAPIView):
    """
    Check the credentials and return the REST Token
    if the credentials are valid and authenticated.
    Calls Django Auth login method to register User ID
    in Django session framework
    Accept the following POST parameters: email, password
    Return the REST Framework Token Object's key.
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer
    response_serializer = TokenSerializer
    token_model = Token

    def process_login(self):
        django_login(self.request, self.user)

    def login(self):
        self.user = self.serializer.validated_data['user']
        self.token = self.token_model.objects.get_or_create(user=self.user)[0]
        self.process_login()

    def get_response(self):
        serializer = self.response_serializer(instance=self.token,
                                              context={'request': self.request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data)
        self.serializer.is_valid(raise_exception=True)
        self.login()
        return self.get_response()


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny, )
    token_model = Token

    def get_response_data(self, user):
        return TokenSerializer(user.auth_token).data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(self.get_response_data(user),
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def perform_create(self, serializer):
        user = serializer.save()
        Token.objects.get_or_create(user=user)
        return user
