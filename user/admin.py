from django.contrib import admin
# from .forms import CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'custom', 'phone', 'address')
    search_fields = ('username', 'email')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Individual Data', {
            'fields': ('custom', 'phone', 'address'),
        }),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    ordering = ('email',)
#
#    def get_form(self, request, obj=None, **kwargs):
#        if obj:  # If editing an existing object
#            return CustomUserChangeForm
#        else:   # If creating a new object
#            return super().get_form(request, obj, **kwargs)
#

    def save_model(self, request, obj, form, change):
        if obj.pk:
            # Existing user, hash the password if changed
            if form.cleaned_data['password']:
                obj.set_password(form.cleaned_data['password'])
        else:
            # New user, set password and hash it
            obj.set_password(obj.password)
        obj.save()


admin.site.register(CustomUser, CustomUserAdmin)
