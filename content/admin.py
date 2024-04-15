from django.contrib import admin
from .models import Video
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class VideoResource(resources.ModelResource):

    class Meta:
        model = Video


class VideoAdmin(ImportExportModelAdmin):
    resource_classes = [VideoResource]
    list_display = ('created_at','title','description')
    search_fields = ('title',)


admin.site.register(Video, VideoAdmin)


    

