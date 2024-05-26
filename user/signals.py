from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from content.models import Video
from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def set_staff_permissions(sender, instance, **kwargs):
    """
    Sets staff permissions for the given CustomUser instance.

    If the CustomUser instance is_staff attribute is True, it grants the following permissions:
    - add_video: Can add video
    - change_video: Can change video
    - delete_video: Can delete video
    - view_video: Can view video
    - add_contenttype: Can add content type
    - change_contenttype: Can change content type
    - delete_contenttype: Can delete content type
    - add_customuser: Can add custom user
    - change_customuser: Can change custom user
    - delete_customuser: Can delete custom user
    - view_customuser: Can view custom user

    If the CustomUser instance is_staff attribute is False, it clears all user permissions.

    :param sender: The sender of the signal.
    :type sender: Any
    :param instance: The instance of CustomUser.
    :type instance: CustomUser
    :param kwargs: Additional keyword arguments.
    """
    if instance.is_staff and not instance.is_superuser:
        model_permissions = [
            ('add_video', 'Can add video', Video),
            ('change_video', 'Can change video', Video),
            ('delete_video', 'Can delete video', Video),
            ('view_video', 'Can view video', Video),
            ('add_contenttype', 'Can add content type', ContentType),
            ('change_contenttype', 'Can change content type', ContentType),
            ('delete_contenttype', 'Can delete content type', ContentType),
            ('add_customuser', 'Can add custom user', CustomUser),
            ('change_customuser', 'Can change custom user', CustomUser),
            ('delete_customuser', 'Can delete custom user', CustomUser),
            ('view_customuser', 'Can view custom user', CustomUser),
        ]
        for codename, name, model_class in model_permissions:
            content_type=ContentType.objects.get_for_model(model_class)
            permission, created = Permission.objects.get_or_create(
                codename=codename,
                content_type=content_type,
                defaults={
                    "name": name,
                }
            )
            if permission not in instance.user_permissions.all():
                instance.user_permissions.add(permission)
    else:
        instance.user_permissions.clear()
