import os
import django_rq
from .tasks import convert480p, convert720p
from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save, post_init


@receiver(post_save, sender=Video)
def video_pos_save(sender, instance, created, **kwargs):
    """
    A signal handler function for renaming thumbnail with same identifier als video_file
    :param sender: The sender of the signal.
    :type sender: Any
    :param instance: The instance being saved.
    :type instance: Any
    :param created: Indicates whether the instance was created (True) or updated (False).
    :type created: bool
    :param kwargs: Additional keyword arguments.
    """
    if not hasattr(instance, '_performing_post_save'):
        instance._performing_post_save = False

    if not instance._performing_post_save:
        instance._performing_post_save = True

        if created or instance.thumbnail_file != instance._original_thumbnail_file:
            if instance.video_file and instance.thumbnail_file:
                video_filename = os.path.basename(instance.video_file.name)
                video_name, video_ext = os.path.splitext(video_filename)
                thumbnail_name = f"{video_name}_thumbnail.jpg"
                current_thumbnail_path = instance.thumbnail_file.path
                new_thumbnail_path = os.path.join(os.path.dirname(current_thumbnail_path), thumbnail_name)
                os.rename(current_thumbnail_path, new_thumbnail_path)
                instance.thumbnail_file.name = os.path.relpath(new_thumbnail_path, 'media')
                instance.save(update_fields=['thumbnail_file'])

        if created:
            queue = django_rq.get_queue('default', autocommit=True)
            queue.enqueue(convert480p, instance.video_file.path)
            queue.enqueue(convert720p, instance.video_file.path)

        instance._performing_post_save = False


@receiver(pre_save, sender=Video)
def update_thumbnail(sender, instance, **kwargs):
    """
    A signal handler function for checking pre save if thumbnail exists and deletes old file if changed
    :param sender: The sender of the signal.
    :type sender: Any
    :param instance: The instance being saved.
    :type instance: Any
    :param kwargs: Additional keyword arguments
    """
    if instance.pk:
        try:
            old_instance = Video.objects.get(pk=instance.pk)
            if old_instance.thumbnail_file != instance.thumbnail_file:
                if old_instance.thumbnail_file:
                    if os.path.exists(old_instance.thumbnail_file.path):
                        os.remove(old_instance.thumbnail_file.path)
        except Video.DoesNotExist:
            pass


@receiver(post_init, sender=Video)
def store_original_thumbnail(sender, instance, **kwargs):
    """
    A signal handler function for creating copy of the thumbnail_file to check whether updated later on
    :param sender: The sender of the signal.
    :type sender: Any
    :param instance: The instance being saved.
    :type instance: Any
    :param kwargs: Additional keyword arguments
    """
    instance._original_thumbnail_file = instance.thumbnail_file


@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kkwargs):
    """
    A signal handler function for deleting video file from filesystem
    when corresponding 'Video' onject is deleted
    :param sender: The sender of the signal.
    :type sender: Any
    :param instance: The instance being saved.
    :type instance: Any
    :param kwargs: Additional keyword arguments
    """
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)

    if instance.video_file:
        base_name, ext = os.path.splitext(instance.video_file.path)
        converted_file_path = f"{base_name}_480p.mp4"
        if os.path.isfile(converted_file_path):
            os.remove(converted_file_path)

    if instance.video_file:
        base_name, ext = os.path.splitext(instance.video_file.path)
        converted_file_path = f"{base_name}_720p.mp4"
        if os.path.isfile(converted_file_path):
            os.remove(converted_file_path)


@receiver(post_delete, sender=Video)
def delete_thumbnail_file(sender, instance, **kwargs):
    """
    A signal handler function for deleting thumbnail file from filesystem
    when corresponing 'Video' onject is deleted
    :param sender: The sender of the signal.
    :type sender: Any
    :param instance: The instance being saved.
    :type instance: Any
    :param kwargs: Additional keyword arguments
    """
    if instance.thumbnail_file:
        if os.path.isfile(instance.thumbnail_file.path):
            os.remove(instance.thumbnail_file.path)
