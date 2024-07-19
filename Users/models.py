import uuid
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from Chess.managers import BaseLayer
class CustomUserManager(BaseUserManager):
    """
    Custom manager for our custom user model.
    """

    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, BaseLayer):
    """
    To store users
    """
    rating = models.BigIntegerField(default=1200)
    full_name = models.TextField(null=True, blank=True)
    agreement_time = models.DateTimeField(null=True, blank=True)
    username= models.CharField(max_length=100, unique=True)
    email = models.EmailField(null=True, blank=True)  # Assuming you may want to use email as well
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    age = models.PositiveIntegerField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f"{self.username or ''}".lstrip()

    class Meta:
        db_table = 'users'
