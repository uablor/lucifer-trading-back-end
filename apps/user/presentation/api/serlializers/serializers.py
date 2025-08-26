# presentation/api/serializers.py
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from apps.user.config.models import User
from django.contrib.auth.models import (Group, Permission)
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(allow_null=True, required=False)
    username = serializers.CharField(
        max_length=150,
        allow_null=True,
        required=False,
        error_messages={
            "invalid": _("This value may contain only letters, numbers and @/./+/-/_ characters."),
            "required": _("This field is required."),
            "blank": _("This field cannot be blank."),
            "null": _("This field cannot be null."),
        },
    )
    email = serializers.EmailField(
        allow_null=True, required=False,
        validators=[UniqueValidator(queryset=User.objects.all(), message="this email already exists.")],
        error_messages={
            "required": _("This field is required."),
            "blank": _("This field cannot be blank."),
            "null": _("This field cannot be null."),
            "invalid": _("This value must be a valid email address."),
        }
    )
    password = serializers.CharField(
        allow_null=True, required=False,
        write_only=True,
        validators=[validate_password],
        error_messages={
            "required": _("This field is required."),
            "blank": _("This field cannot be blank."),
            "null": _("This field cannot be null."),
        }
    )
    is_active = serializers.BooleanField( allow_null=True, required=False)
    is_staff = serializers.BooleanField( allow_null=True, required=False)
    is_superuser = serializers.BooleanField( allow_null=True, required=False)
    groups = serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.all(), allow_null=True, required=False)
    user_permissions = serializers.PrimaryKeyRelatedField(many=True, queryset=Permission.objects.all(), allow_null=True, required=False)


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
        