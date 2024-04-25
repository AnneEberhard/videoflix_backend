from rest_framework import serializers
from .models import Video

class VideoSerializer(serializers.ModelSerializer):
    thumbnail_file_url = serializers.SerializerMethodField()
    video_file_url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'thumbnail_file_url', 'video_file_url', 'genre']

    def get_thumbnail_file_url(self, obj):
        if obj.thumbnail_file:
            return self.context['request'].build_absolute_uri(obj.thumbnail_file.url)
        return None

    def get_video_file_url(self, obj):
        if obj.video_file:
            return self.context['request'].build_absolute_uri(obj.video_file.url)
        return None
