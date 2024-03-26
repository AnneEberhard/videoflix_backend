from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


"""
This serializer handles the user and assures a correct password is created
"""
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #fields = '__all__'
        exclude = ['first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create (self, validated_data):
        return User.objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        
        return user
