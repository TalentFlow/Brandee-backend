from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)


class UserManager(BaseUserManager):


    

    def create_user(self, email,first_name,last_name,  password, **other_fields):

        if not email:
            raise ValueError('You must provide an email address')
        if not first_name :
            raise ValueError('First Name should not be none.')
        if not last_name:
            raise ValueError('Last Name should not be none.')
        if not password:
            raise ValueError('Password should not be none.')

        email = self.normalize_email(email)
        user = self.model(email=email, 
        first_name=first_name,last_name=last_name, is_active=True,
         **other_fields)
        user.set_password(password)
        user.save()
        return user



    def create_superuser(self, email,first_name,last_name, password=None, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        # other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')
        

        return self.create_user(email, 
        first_name, last_name,
        password, **other_fields)
    

class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=255, unique=True, db_index=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name',]

    def __str__(self):
        return self.email

    def tokens(self):
        return ''