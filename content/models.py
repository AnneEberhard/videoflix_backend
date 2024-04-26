from datetime import date
from django.db import models

class Video(models.Model):
    GENRE_CHOICES = [
        ('Dystopia', 'Dystopia'),
        ('Fantasy', 'Fantasy'),
        ('Historical', 'Historical'),
        ('Spy', 'Spy'),
        ('Contemporary', 'Contemporary'),
    ]

    created_at = models.DateField(default=date.today)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=500)
    video_file = models.FileField(upload_to='videos', blank=True, null=True)
    thumbnail_file = models.FileField(upload_to='thumbnails', blank=True, null=True)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, default='')


    def __str__(self):
        return self.title
