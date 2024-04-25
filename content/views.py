from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from .serializer import VideoSerializer
from .models import Video
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.core.cache import cache

class CustomTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'

    def authenticate_credentials(self, key):
        # Ignore 'Bearer' prefix if present
        if key.startswith(self.keyword + ' '):
            key = key[len(self.keyword) + 1:]

        return super().authenticate_credentials(key)

# is defined in the settings
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

@api_view(['GET'])
#@authentication_classes([CustomTokenAuthentication])
#@permission_classes([IsAuthenticated])
@cache_page(CACHE_TTL)
def video_overview(request):
    cache_key = 'cache_page_videos_overview'
    cached_data = cache.get(cache_key)

    if not cached_data:
        uploaded_videos = Video.objects.all()
        serializer = VideoSerializer(uploaded_videos, many=True, context={'request': request})
        cached_data = serializer.data
        cache.set(cache_key, cached_data, CACHE_TTL)
    else:
        serializer = VideoSerializer(cached_data, many=True, context={'request': request})

    return JsonResponse(serializer.data, safe=False)

