from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = '__all__'
    
#   def __init__(self, *args, **kwargs):
#       super().__init__(*args, **kwargs)
#       if not self.instance.is_superuser:
#           self.fields['user_permissions'].widget = forms.HiddenInput()