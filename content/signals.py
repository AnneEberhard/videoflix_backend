import os

from .tasks import convert480p, convert720p
from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

@receiver(post_save, sender=Video)
def video_pos_save(sender, instance, created, **kwargs):
    print('Video')
    if created:
        print('new video created')
        convert480p(instance.video_file.path)
        convert720p(instance.video_file.path)


@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kkwargs):
    """
    Deletes file from filesystem
    when corresponing 'Video' onject is deleted
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