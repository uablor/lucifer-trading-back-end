# presentation/api/serializers.py
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from apps.user.config.models import User
from django.contrib.auth.models import (Group, Permission)
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from apps.user.presentation.api.serlializers.serializers import UserSerializer

class UserRegisterSerializer(UserSerializer):
    password2 = serializers.CharField(required=True, write_only=True,
        error_messages={
            "required": _("This field is required."),
            "blank": _("This field cannot be blank."),
            "null": _("This field cannot be null."),
        }
    )

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(_("Passwords don't match"))
        return data


class UserLoginSerializer(serializers.Serializer):
    password = serializers.CharField(required=True,
        error_messages={
            "required": _("This field is required."),
            "blank": _("This field cannot be blank."),
            "null": _("This field cannot be null."),
        }
    )
    email = serializers.EmailField(required=True,
        error_messages={
            "required": _("This field is required."),
            "blank": _("This field cannot be blank."),
            "null": _("This field cannot be null."),
            "invalid": _("This value must be a valid email address."),
        }
    )


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True,
        error_messages={
            "required": _("This field is required."),
            "blank": _("This field cannot be blank."),
            "null": _("This field cannot be null."),
        }
    )
    
    
class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True,
        error_messages={
            "required": _("This field is required."),
            "blank": _("This field cannot be blank."),
            "null": _("This field cannot be null."),
            "invalid": _("This value must be a valid email address."),
        }
    )
    
    
class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True,
        error_messages={
            "required": _("This field is required."),
            "blank": _("This field cannot be blank."),
            "null": _("This field cannot be null."),
        }
    )
    new_password = serializers.CharField(required=True,
        error_messages={
            "required": _("This field is required."),
            "blank": _("This field cannot be blank."),
            "null": _("This field cannot be null."),
        }
    )
    
    confirm_password = serializers.CharField(required=True,
        error_messages={
            "required": _("This field is required."),
            "blank": _("This field cannot be blank."),
            "null": _("This field cannot be null."),
        }
    )
    
    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError(_("Passwords don't match"))
        return data
    
    
class PasswordResetSerializer(serializers.Serializer):
    
    password = serializers.CharField(write_only=True, required = True, validators = [validate_password])
    confirm_password = serializers.CharField(write_only=True, required = True)
        
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        data.pop('confirm_password')
        return data

