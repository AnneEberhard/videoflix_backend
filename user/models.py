from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

   
class UserManager(BaseUserManager):
    """
    The dadpated Manager for users
    """
    use_in_migration = True

    def _create_user(self, email, password, **extra_fields):
        """
        private method, checks if email exists in the right format
        creates user und hashes password
        returns user
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
        public method, sets extra fields and calls on _create_user() to create as defined above
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False) 
        
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """
        public method to set extra fields for super user, calling on _create_user() as defined above
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)  

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    The adapted model for users
    """
 
    custom = models.CharField(max_length=1000, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=150, blank=True)

    objects = UserManager()
    


