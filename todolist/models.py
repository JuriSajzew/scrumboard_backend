import datetime
from django.conf import settings
from django.db import models


# Create your views here.
LOW = 'low'
MEDIUM = 'medium'
HIGH = 'high'
PRIORITY_CHOICES = [
    (LOW, 'Low'),
    (MEDIUM, 'Medium'),
    (HIGH, 'High'), 
]
class Todolist(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=150)
    created_at = models.DateField(default=datetime.date.today)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    priority = models.CharField(max_length=6, choices = PRIORITY_CHOICES, default = MEDIUM)
    dateline = models.DateField(null=True, blank=True)
    state = models.CharField(max_length=30, null=True, blank=True)
    
    def __str__(self):
        return f'{self.id} {self.title}'

from django.contrib.auth.models import BaseUserManager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import Group, Permission
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Hier werden die related_names gesetzt, um die Konflikte zu lösen
    groups = models.ManyToManyField(Group, blank=True, related_name='customuser_set', verbose_name='groups')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='customuser_set', verbose_name='user permissions')

    def __str__(self):
        return self.email