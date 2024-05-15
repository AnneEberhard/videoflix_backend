from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.response import Response
from .serializer import LoginViewSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse

def home_view(request):
    """
    Thies views handles a landing page for the overall project
    """
    context = {
        'frontend_url': settings.FRONTEND_URL,
        'backend_url': settings.BACKEND_URL,
    }
    return render(request, "home.html", context)


@method_decorator(csrf_exempt, name='dispatch')
class RegistrationView(generics.CreateAPIView):
    """
    This view handles user registration and sends an activation email.
    Endpoints:
    - POST /register: Registers a new user and sends an activation email.
    """
    @csrf_exempt
    def post(self, request):
        print('register')
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')

        if get_user_model().objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        User = get_user_model()
        user = User.objects.create_user(email=email, username=username, password=password, is_active=False)
        user.save()

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        activation_link = f"{settings.BACKEND_URL}/activate/{uidb64}/{token}/"

        subject = 'Account Activation'
        html_message = render_to_string('activation_email.html', {'activation_link': activation_link})
        plain_message = strip_tags(html_message)
        from_email = 'noreply@videoflix.com'
        to_email = [email]
        print(activation_link)
        send_mail(subject, plain_message, from_email, to_email, html_message=html_message)

        return Response({'success': 'Account created. Please check your email to activate your account.'}, status=status.HTTP_201_CREATED)


class ActivationView(View):
    """
    This view handles user activation after clicking on the activation link.
    Endpoints:
    - GET /activate/<uidb64>/<token>/: Activates a user account.
    """
    def get(self, request, uidb64, token):
        User = get_user_model()
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect(reverse('activation_success'))
        else:
            return redirect(reverse('activation_failure'))


class ActivationFailureView(TemplateView):
    """
    This view is displayed when user activation fails.
    """
    template_name = 'activation_failure.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['frontend_url'] = settings.FRONTEND_URL

        return context


class ActivationSuccessView(TemplateView):
    """
    This view is displayed when user activation is successful.
    """
    template_name = 'activation_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['frontend_url'] = settings.FRONTEND_URL

        return context


class LoginView(ObtainAuthToken):
    """
    This view handles user login and token generation.
    Endpoints:
    - POST /login: Logs in the user and generates a token.
    """
    serializer_class = LoginViewSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        if not user.is_active:
            return Response({'error': 'Account not activated'}, status=status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key,
                         'user_id': user.pk,
                         'username': user.username,
                         'email': user.email})


class LogoutView(APIView):
    """
    This view handles user logout.
    Endpoints:
    - POST /logout: Logs out the user and deletes the authentication token.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        request.auth.delete()
        cache.delete('cache_page_videos_overview')
        return Response({'message': 'Logout erfolgreich'}, status=status.HTTP_200_OK)


class ForgotView(APIView):
    """
    This view handles the request for resetting the user's password and sends a reset password link via email.
    Endpoints:
    - POST /forgot: Sends a password reset link to the user's email.
    """
    def post(self, request):
        email = request.data.get('email')

        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=400)

        token_generator = PasswordResetTokenGenerator()
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)

        reset_password_link = f"{settings.FRONTEND_URL}/reset?uidb64={uidb64}&token={token}/"

        subject = 'Password Reset'
        html_message = render_to_string('reset_password_email.html', {'reset_password_link': reset_password_link})
        plain_message = strip_tags(html_message)
        from_email = 'noreply@videoflix.com'
        to_email = [email]

        send_mail(subject, plain_message, from_email, to_email, html_message=html_message)
        print(reset_password_link)

        return JsonResponse({'success': 'Reset password link sent'}, status=200)


class ResetView(APIView):
    """
    This view handles password reset after clicking on the reset password link.
    Endpoints:
    - POST /reset/<uidb64>/<token>/: Resets the user's password.
    """
    def post(self, request, uidb64, token):
        new_password = request.data.get('password')

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            return JsonResponse({'error': 'Invalid user or token'}, status=400)

        if not PasswordResetTokenGenerator().check_token(user, token):
            return JsonResponse({'error': 'Invalid token'}, status=400)

        user.set_password(new_password)
        user.is_active = True
        user.save()

        return JsonResponse({'success': 'Password successfully reset'}, status=200)
