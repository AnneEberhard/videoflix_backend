from django import apps
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
   

class UserManager(BaseUserManager):
    use_in_migration = True

    def _create_user(self, email, password, **extra_fields):
        """
        Erstellt und speichert einen Benutzer mit der gegebenen E-Mail-Adresse und Passwort.
        """
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Erstellt und speichert einen Benutzer mit der gegebenen E-Mail-Adresse und Passwort.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False) 
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Erstellt und speichert einen Superuser mit der gegebenen E-Mail-Adresse und Passwort.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)  

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self._create_user(email, password, **extra_fields)


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


