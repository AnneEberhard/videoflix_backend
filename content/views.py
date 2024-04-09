from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from .serializer import VideoSerializer
from .models import Video
from rest_framework.decorators import api_view, authentication_classes, permission_classes



# is defined in the settings
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@cache_page(CACHE_TTL)
def video_overview(request):
    uploaded_videos = Video.objects.all()
    serializer = VideoSerializer(uploaded_videos, many=True)
    return JsonResponse(serializer.data, safe=False)  
