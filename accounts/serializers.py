from rest_framework import serializers, exceptions
from django.utils import timezone
from datetime import timedelta
from django.core.validators import RegexValidator
from django.contrib import auth

from .models import CustomUser

from .extension import utils

class UserAuthSerializer(serializers.Serializer):
    phone_regex = RegexValidator(regex=r'^\+\d{8,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = serializers.CharField(validators=[phone_regex], max_length=16)

    password = serializers.CharField(required=False)

    invitation_code = serializers.CharField(required=False)

    def _set_otp(self):
        return (utils.get_random_string(4),
                timezone.now() + timedelta(minutes=1))


    def create(self, validated_data):
        validated_data["password"], validated_data["otp_valid_until"] = self._set_otp()
        user = CustomUser.objects.create(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.password, instance.otp_valid_until = self._set_otp()
        instance.save()
        return instance
    
    def is_password_valid(self, validated_data, raise_exception=False):
        if "password" in validated_data:
            user = CustomUser.objects.filter(**validated_data).first()
            if user and user.password == validated_data["password"]:
                return True

        if raise_exception:
            raise exceptions.ValidationError("Incorrect password or phone_number")
        

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            'phone_number',
            'invited_by',
            'invitation_code',
        ]
        read_only_fields = [
            'phone_number',
            'invitation_code',
            ]

