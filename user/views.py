from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .serializer import LoginViewSerializer, UserSerializer
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



"""
This view handles login
"""
class LoginView(ObtainAuthToken):
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


"""
This view handles logout
"""
class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        request.auth.delete()
        cache.delete('cache_page_videos_overview')
        return Response({'message': 'Logout erfolgreich'}, status=status.HTTP_200_OK)


"""
This view handles registering a new user and sends out an email containing a unique link for activation
"""
class RegistrationView(generics.CreateAPIView):
    #serializer_class = UserSerializer

    def post(self, request):
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
    
"""
This view handles activating a new user after clicking on the unique link
"""
class ActivationView(View):
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

"""
This view is for the user in case of activation failure 
"""
class ActivationFailureView(TemplateView):
    template_name = 'activation_failure.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['frontend_url'] = settings.FRONTEND_URL

        return context

"""
This view is for the user in case of activation success 
"""
class ActivationSuccessView(TemplateView):
    template_name = 'activation_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['frontend_url'] = settings.FRONTEND_URL

        return context


"""
This view checks if the email send from the frontend is existent in the user db and 
sends an email containing an unique link including token and uidb for the frontend reset interface
"""
class ForgotView(APIView):
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
    

"""
This view resets the password in the backend and sets the user on active
"""
class ResetView(APIView):
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




#lass RegistrationView2(generics.CreateAPIView):
#   serializer_class = UserSerializer 
#
#   def post(self, request, *args, **kwargs):
#       email = request.data.get('email')
#       if User.objects.filter(email=email).exists():
#           return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
#
#       user_serializer = self.get_serializer(data=request.data)
#       user_serializer.is_valid(raise_exception=True)
#       user = user_serializer.save()
#
#       token_generator = default_token_generator
#       uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
#       token = token_generator.make_token(user)
#
#       activation_link = f"http://127.0.0.1:5500/activate/?uidb64={uidb64}&token={token}"
#       #activation_link = f"https://yourdomain.com/activate/?uidb64={uidb64}&token={token}"
#
#       subject = 'Account Activation'
#       html_message = render_to_string('activation_email.html', {'activation_link': activation_link})
#       plain_message = strip_tags(html_message)  # Strip HTML tags for plain text email
#       from_email = 'noreply@videoflix.com'
#       to_email = [email]
#
#       send_mail(subject, plain_message, from_email, to_email, html_message=html_message)
#
#       return Response({'success': 'Account created. Please check your email to activate your account.'}, status=status.HTTP_201_CREATED)
#
   
#
#class ActivationView(View):
#    def get(self, request, uidb64, token):
#        User = get_user_model()
#        try:
#            uid = urlsafe_base64_decode(uidb64).decode()
#            user = User.objects.get(pk=uid)
#        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#            user = None
#
#        if user is not None and default_token_generator.check_token(user, token):
#            user.is_active = True
#            user.save()
#            # Redirect to a success page or whatever you need
#            return redirect(reverse('activation_success'))
#        else:
#            # Redirect to a failure page or whatever you need
#            return redirect(reverse('activation_failure'))
        
