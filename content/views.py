from django.conf import settings
from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import VideoSerializer
from .models import Video



# is defined in the settings
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

class VideoView(APIView):

   # @cache_page(CACHE_TTL)
    def get(self, request):
        uploaded_videos = Video.objects.all()
        serializer = VideoSerializer(uploaded_videos, many=True)
        return Response(serializer.data)    
