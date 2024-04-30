from rest_framework import serializers
from user.models import CustomUser
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for handling user data and ensuring correct password creation.

    This serializer is responsible for handling user data and ensuring that a correct password is created.
    It excludes the 'first_name' and 'last_name' fields from the serialization process and marks the 'password'
    field as write-only.

    Methods:
    - create: Creates a new user with the provided validated data.
    - update: Updates an existing user instance with the provided validated data, including password handling.

    """
    class Meta:
        model = CustomUser
        exclude = ['first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class LoginViewSerializer(serializers.Serializer):
    """
    Serializer for handling authentication tokens required for login.

    This serializer is responsible for handling authentication tokens and is needed for the creation
    of a token for login. It includes fields for email and password. The email field is of type EmailField,
    while the password field is of type CharField with the input type set to 'password' for secure entry.
    Serializer is called in LogInView: serializer = self.get_serializer(data=request.data)

    Methods:
    - validate: Validates the email and password fields and returns the user instance if authentication is successful.
    """
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = get_user_model().objects.filter(email=email).first()

            if user and user.check_password(password):
                attrs['user'] = user
                return attrs

        msg = 'Unable to log in with provided credentials.'
        raise serializers.ValidationError(msg)
