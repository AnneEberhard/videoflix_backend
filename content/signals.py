import os
import django_rq
from .tasks import convert480p, convert720p
from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

@receiver(post_save, sender=Video)
def video_pos_save(sender, instance, created, **kwargs):
    print('Video')
    if created:
        if instance.video_file and instance.thumbnail_file:
            video_filename = os.path.basename(instance.video_file.name)
            video_name, video_ext = os.path.splitext(video_filename)
            thumbnail_name = f"{video_name}_thumbnail{video_ext}"
            current_thumbnail_path = instance.thumbnail_file.path
            new_thumbnail_path = os.path.join(os.path.dirname(current_thumbnail_path), thumbnail_name)
            os.rename(current_thumbnail_path, new_thumbnail_path)
            instance.thumbnail_file.name = os.path.relpath(new_thumbnail_path, 'media')
            instance.save(update_fields=['thumbnail_file'])
        print('new video created')
        queue = django_rq.get_queue('default', autocommit=True) #default ist die einzige Art, die in den settings definiert ist
        queue.enqueue(convert480p, instance.video_file.path) # ersetzt convert480p(instance.video_file.path)
        queue.enqueue(convert720p, instance.video_file.path) #convert720p(instance.video_file.path)


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

@receiver(post_delete, sender=Video)
def delete_thumbnail_file(sender, instance, **kwargs):
    if instance.thumbnail_file:
        if os.path.isfile(instance.thumbnail_file.path):
            os.remove(instance.thumbnail_file.path)