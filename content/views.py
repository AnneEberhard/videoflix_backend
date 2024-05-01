from django.conf import settings
from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from .serializer import VideoSerializer
from .models import Video
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.core.cache import cache
from django.http import FileResponse
import os

class CustomTokenAuthentication(TokenAuthentication):
    """
    Custom token-based authentication class.

    This class extends the TokenAuthentication class provided by Django REST Framework to ensure logged-in status.
    It overrides the `authenticate_credentials` method to handle the authentication process and ignores the 'Bearer'
    prefix if present in the authentication token.

    Attributes:
    - keyword: The keyword used to identify the token type in the authentication header.
               Default is 'Bearer'.

    Methods:
    - authenticate_credentials: Authenticates the provided token credentials.
    """
    keyword = 'Bearer'

    def authenticate_credentials(self, key):
        # Ignore 'Bearer' prefix if present
        if key.startswith(self.keyword + ' '):
            key = key[len(self.keyword) + 1:]

        return super().authenticate_credentials(key)


# is defined in the settings
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@api_view(['GET'])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
@cache_page(CACHE_TTL)
def video_overview(request):
    """
    Returns video data for uploaded videos.

    This view function returns data for uploaded videos. If cached data exists, it returns the cached data
    to improve performance.

    Endpoints:
    - GET /video_overview: Returns video data.
    """
    cache_key = 'cache_page_videos_overview'
    cached_data = cache.get(cache_key)

    if not cached_data:
        uploaded_videos = Video.objects.all()
        print('non-cache')
        print(uploaded_videos)
        serializer = VideoSerializer(uploaded_videos, many=True, context={'request': request})
        cached_data = serializer.data
        cache.set(cache_key, cached_data, CACHE_TTL)
    else:
        print('cache')
        print(cached_data)
        # Beware: Cave cached_data cannot be serialized twice!

    return JsonResponse(cached_data, safe=False)

#@authentication_classes([CustomTokenAuthentication])
#@permission_classes([IsAuthenticated])
def speedtest_file_view(request):
    file_path = os.path.join(settings.SPEEDTEST_FILES_ROOT, 'data_1mb.test')
    print(file_path)
    return FileResponse(open(file_path, 'rb'))
