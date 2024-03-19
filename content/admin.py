from django.contrib import admin
from .models import Video

class videoAdmin(admin.ModelAdmin):
    list_display = ('created_at','title','description')
    search_fields = ('title',)

admin.site.register(Video)
