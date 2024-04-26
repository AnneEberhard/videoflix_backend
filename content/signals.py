import os
from django.conf import settings
import django_rq
from .tasks import convert480p, convert720p
from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save, post_init
from django.core.files import File

@receiver(post_save, sender=Video)
def video_pos_save(sender, instance, created, **kwargs):
    if created:
        if instance.video_file and instance.thumbnail_file:
            video_filename = os.path.basename(instance.video_file.name)
            video_name, video_ext = os.path.splitext(video_filename)
            thumbnail_name = f"{video_name}_thumbnail.jpg"
            current_thumbnail_path = instance.thumbnail_file.path
            new_thumbnail_path = os.path.join(os.path.dirname(current_thumbnail_path), thumbnail_name)
            os.rename(current_thumbnail_path, new_thumbnail_path)
            instance.thumbnail_file.name = os.path.relpath(new_thumbnail_path, 'media')
            instance.save(update_fields=['thumbnail_file'])
        
        queue = django_rq.get_queue('default', autocommit=True) #default ist die einzige Art, die in den settings definiert ist
        queue.enqueue(convert480p, instance.video_file.path) # ersetzt convert480p(instance.video_file.path)
        queue.enqueue(convert720p, instance.video_file.path) #convert720p(instance.video_file.path)

@receiver(pre_save, sender=Video)
def update_thumbnail(sender, instance, **kwargs):
    if instance.pk:  # Prüfen, ob es sich um ein vorhandenes Objekt handelt
        try:
            old_instance = Video.objects.get(pk=instance.pk)
            if old_instance.thumbnail_file != instance.thumbnail_file:
                # Wenn das Thumbnail geändert wurde, entferne die alte Datei
                if old_instance.thumbnail_file:
                    if os.path.exists(old_instance.thumbnail_file.path):
                        os.remove(old_instance.thumbnail_file.path)
        except Video.DoesNotExist:
            pass

@receiver(post_init, sender=Video)
def store_original_thumbnail(sender, instance, **kwargs):
    instance._original_thumbnail_file = instance.thumbnail_file

@receiver(post_save, sender=Video)
def save_thumbnail(sender, instance, created, **kwargs):
    if created or instance.thumbnail_file != instance._original_thumbnail_file:
        # Wenn das Objekt neu erstellt wird oder das Thumbnail geändert wurde,
        # speichere das neue Thumbnail
        if instance.thumbnail_file:
            video_filename = os.path.basename(instance.video_file.name)
            video_name, _ = os.path.splitext(video_filename)
            thumbnail_name = f"{video_name}_thumbnail.jpg"
            new_thumbnail_path = os.path.join(settings.MEDIA_ROOT, 'thumbnails', thumbnail_name)

            with open(instance.thumbnail_file.path, 'rb') as new_thumbnail:
                with open(new_thumbnail_path, 'wb') as new_thumbnail_file:
                    new_thumbnail_file.write(new_thumbnail.read())

            instance.thumbnail_file.name = os.path.relpath(new_thumbnail_path, settings.MEDIA_ROOT)
            instance.save(update_fields=['thumbnail_file'])


@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kkwargs):
    """
    Deletes video file from filesystem
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
    """
    Deletes thumbnail file from filesystem
    when corresponing 'Video' onject is deleted
    """
    if instance.thumbnail_file:
        if os.path.isfile(instance.thumbnail_file.path):
            os.remove(instance.thumbnail_file.path)