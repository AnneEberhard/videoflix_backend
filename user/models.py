from django import apps
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password
#from django.contrib.auth.models import BaseUserManager
#from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)  

    USERNAME_FIELD = 'email'  


#class UserManager(BaseUserManager):
#    use_in_migration = True
#    def _create_user(self, username, email, password, **extra_fields):
#        if not username:
#            raise ValueError("The given username must be set")
#        email = self.normalize_email(email)
#        GlobalUserModel = apps.get_model(
#            self.model._meta.app_label, self.model._meta.object_name
#        )
#        username = GlobalUserModel.normalize_username(username)
#        user = self.model(username=username, email=email, **extra_fields)
#        user.password = make_password(password)
#        user.save(using=self._db)
#        return user
#
#    def create_user(self, username, email=None, password=None, **extra_fields):
#        extra_fields.setdefault("is_staff", False)
#        extra_fields.setdefault("is_superuser", False)
#        return self._create_user(username, email, password, **extra_fields)
    

#
#class UserManager(BaseUserManager):
#   use_in_migration = True
#
#   def _create_user(self, email, password, **extra_fields):
#       """
#       Erstellt und speichert einen Benutzer mit der gegebenen E-Mail-Adresse und Passwort.
#       """
#       if not email:
#           raise ValueError(_('The Email field must be set'))
#       email = self.normalize_email(email)
#       user = self.model(email=email, **extra_fields)
#       user.set_password(password)
#       user.save(using=self._db)
#       return user
#
#   def create_user(self, email, password=None, **extra_fields):
#       """
#       Erstellt und speichert einen Benutzer mit der gegebenen E-Mail-Adresse und Passwort.
#       """
#       extra_fields.setdefault('is_staff', False)
#       extra_fields.setdefault('is_superuser', False)
#       return self._create_user(email, password, **extra_fields)
#
#   def create_superuser(self, email, password=None, **extra_fields):
#       """
#       Erstellt und speichert einen Superuser mit der gegebenen E-Mail-Adresse und Passwort.
#       """
#       extra_fields.setdefault('is_staff', True)
#       extra_fields.setdefault('is_superuser', True)
#
#       if extra_fields.get('is_staff') is not True:
#           raise ValueError(_('Superuser must have is_staff=True.'))
#       if extra_fields.get('is_superuser') is not True:
#           raise ValueError(_('Superuser must have is_superuser=True.'))
#
#       return self._create_user(email, password, **extra_fields)


