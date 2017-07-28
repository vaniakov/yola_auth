from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):

    EDITABLE_FIELDS = ('first_name', 'last_name')

    email = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'first_name', 'last_name',
                  'is_staff', 'password', 'confirm_password',)
        read_only_fields = ('email', 'is_staff')

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        for field_name in self.EDITABLE_FIELDS:
            if validated_data.get(field_name):
                setattr(instance, field_name, validated_data.get(field_name))
        instance.save()

        password = validated_data.get('password')
        confirm_password = validated_data.get('confirm_password')

        if password and confirm_password and password == confirm_password:
            instance.set_password(password)
            instance.save()

        return instance
