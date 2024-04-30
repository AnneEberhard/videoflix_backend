from rest_framework import serializers
from .models import Video


class VideoSerializer(serializers.ModelSerializer):
    """
    Main serializer used when videos are called for from frontend
    """
    thumbnail_file_url = serializers.SerializerMethodField()
    video_file_url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'thumbnail_file_url', 'video_file_url', 'genre']

    def get_file_url(self, obj, file_attribute):
        """
        Builds absolute URL to be used in frontend later on.
        Request offers info on how to build the URL.
        :param obj: The object containing the file attribute.
        :type obj: Any
        :param file_attribute: The name of the file attribute.
        :type file_attribute: str
        :return: The absolute URL of the file, or None if the file attribute is not found or is empty.
        :rtype: str or None
        """
        file_instance = getattr(obj, file_attribute)
        if file_instance:
            return self.context['request'].build_absolute_uri(file_instance.url)
        return None

    def get_thumbnail_file_url(self, obj):
        """
        Builds an absolute URL for the thumbnail file of the given object.
        :param obj: The object containing the thumbnail file.
        :type obj: Any
        :return: The absolute URL of the thumbnail file, or None if the thumbnail file is not found or is empty.
        :rtype: str or None
        """
        return self.get_file_url(obj, 'thumbnail_file')

    def get_video_file_url(self, obj):
        """
        Builds an absolute URL for the video file of the given object.
        :param obj: The object containing the video file.
        :type obj: Any
        :return: The absolute URL of the video file, or None if the video file is not found or is empty.
        :rtype: str or None
        """
        return self.get_file_url(obj, 'video_file')
