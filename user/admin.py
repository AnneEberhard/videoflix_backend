from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm


class UserResource(resources.ModelResource):

    class Meta:
        model = CustomUser

#@admin.register(CustomUser)
class CustomUserAdmin(ImportExportModelAdmin):
    add_form = CustomUserCreationForm
    resource_class = UserResource
    list_display = ('id', 'username', 'email')  
    search_fields = ('username', 'email')
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Individual Data',
            {
                'fields': (
                    'custom',
                    'phone',
                    'address',
                )
            }
        )
    )


admin.site.register(CustomUser, CustomUserAdmin)  

