from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .serializer import UserSerializer
from django.contrib.auth.models import User

from .serializer import UserSerializer

"""
This view handles registering a new user
"""
class RegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer 

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=400)
        return self.create(request, *args, **kwargs)

