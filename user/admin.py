from django.contrib import admin
from django.contrib.auth.models import User
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class UserResource(resources.ModelResource):

    class Meta:
        model = User


class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource
    list_display = ('id', 'username', 'email')  
    search_fields = ('username', 'email')

admin.site.unregister(User)  
admin.site.register(User, UserAdmin)  

