from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from content.models import Video
from .models import CustomUser  

@receiver(post_save, sender=CustomUser)
def set_staff_permissions(sender, instance, **kwargs):
    print('signal')
    if instance.is_staff:
        print('yes')
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
            permission, created = Permission.objects.get_or_create(
                codename=codename,
                name=name,
                content_type=ContentType.objects.get_for_model(model_class)
            )
            if permission not in instance.user_permissions.all():
                instance.user_permissions.add(permission)
    else:
        print('no')
        instance.user_permissions.clear()
