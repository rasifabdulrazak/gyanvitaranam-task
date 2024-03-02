from django.contrib import admin
from .models import Company,Employee,ProfilePic
from django.utils.html import format_html


class ImageAdmin(admin.ModelAdmin):
    """This class inherits ModelAdmin features """

    def image_tag(self, obj):
        """This function render images in admin panel"""
        return format_html('<img src="{}" style="max-width:500px; max-height:500px"/>'.format(obj.profile_photo.url))

    image_tag.short_description = 'Image'
    list_display = ['image_tag',]


# Register your models here.
admin.site.register(Company)
admin.site.register(Employee)
admin.site.register(ProfilePic,ImageAdmin)


