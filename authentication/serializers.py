from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers, exceptions
from rest_framework.authtoken.models import Token
from users.models import User as UserModel


class TokenSerializer(serializers.ModelSerializer):
    """
    Serializer for Token model.
    """

    class Meta:
        model = Token
        fields = ('key',)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_blank=False)
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        username = UserModel.objects.get(email=email).get_username()
        user = authenticate(username=username, password=password)

        if user:
            if not user.is_active:
                msg = 'User account is disabled.'
                raise exceptions.ValidationError(msg)
        else:
            msg = 'Unable to log in with provided credentials.'
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        if UserModel.objects.filter(email=data['email'],
                                    username=data['username']).exists():
            raise serializers.ValidationError(
                "A user is already registered with this e-mail address.")
        return data

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password': self.validated_data.get('password', ''),
            'email': self.validated_data.get('email', '')
        }

    def save(self, request, **kwargs):
        return UserModel.objects.create_user(**self.get_cleaned_data())
