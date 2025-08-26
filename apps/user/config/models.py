# apps/user/config/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext as _
from model_utils.models import SoftDeletableModel, TimeStampedModel
from django.db import transaction
from apps.user.config.utils import profile_image_storage, validate_image_extension, validate_max_file_size
class UserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email field must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username or email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    @transaction.atomic
    def create_superuser(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verify", True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        user = self.create_user(email, username, password, **extra_fields)
        return user

class SoftDeletableUserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_removed=False)  # หรือใช้ is_deleted ของ SoftDeletableModel

    def get_by_natural_key(self, email):
        return self.get(**{self.model.USERNAME_FIELD: email})
    
    
class User(SoftDeletableModel,AbstractUser, TimeStampedModel):
    first_name = None 
    last_name = None
    username = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    is_verify = models.BooleanField(default=False)
    is_2fa_enabled = models.BooleanField(default=False)
    avatar = models.FileField(
        upload_to=profile_image_storage,
        validators=[validate_image_extension, validate_max_file_size],
        blank=True,
        null=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    objects = SoftDeletableUserManager()
    def __str__(self):
        return self.username or self.email
