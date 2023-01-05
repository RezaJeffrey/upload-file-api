from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model, login
User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name',
            'username', 'email', 'password'
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, **validated_data):
        user = User.objects.create_user(
            **validated_data
        )
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name',
            'username', 'email'
        )

    def create(self, **validated_data):
        user = User.objects.create_user(
            **validated_data
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name', 'last_name',
            'username', 'email',
            'nationality', 'phone_number',
            'phone_is_verified', 'email_is_verified',
        )


class ChangeUserPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('password', 'new_password', 'new_password_confirm')

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({'new_password': 'passwords must match'})
        return attrs

    def validate_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({'password': 'enter your current password properly'})
        return value

    def update(self, instance, validated_data):
        request = self.context['request']
        instance.set_password(validated_data['new_password'])
        instance.save()
        login(request, instance)
        return instance
