"""
URL configuration for videoflix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from user.views import ActivationView, ForgotView, LoginView, LogoutView, RegistrationView, ActivationSuccessView, ActivationFailureView, ResetView
from content.views import video_overview

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('videos/', video_overview, name='videos'),
    path('django-rq/', include('django_rq.urls')),
    path('activate/<uidb64>/<token>/', ActivationView.as_view(), name='activate'),
    path('activation/success/', ActivationSuccessView.as_view(), name='activation_success'),
    path('activation/failure/', ActivationFailureView.as_view(), name='activation_failure'),
    path('forgot/', ForgotView.as_view(), name='forgot'),
    path('reset/<uidb64>/<token>/', ResetView.as_view(), name='password_reset_confirm'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
