from django.contrib import admin
from media_app.models import File,Image
class FileAdmin(admin.ModelAdmin):

    list_display = ('caption',)


admin.site.register(File, FileAdmin)
class ImageAdmin(admin.ModelAdmin):

    list_display = ('caption',)


admin.site.register(Image, ImageAdmin)
# Register your models here.
