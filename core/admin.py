from django.contrib import admin
from .models import Company, Employee, ProfilePic
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from .resource import EmployeeResource


class ImageAdmin(admin.ModelAdmin):
    """This class inherits ModelAdmin features"""

    def image_tag(self, obj):
        """This function render images in admin panel"""
        return format_html(
            '<img src="{}" style="max-width:500px; max-height:500px"/>'.format(
                obj.profile_photo.url
            )
        )

    image_tag.short_description = "Image"
    list_display = [
        "image_tag",
    ]


class CustomEmployeeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = EmployeeResource

    def get_import_form(self):
        """
        Return an extra field with resource form, named company_id
        """
        from django import forms
        from import_export.forms import ImportForm

        class CustomImportForm(ImportForm):
            company_id = forms.ModelChoiceField(
                queryset=Company.objects.all()
            )  # Assuming Company is the related model

        return CustomImportForm


# Register your models here.
admin.site.register(Company)
admin.site.register(Employee, CustomEmployeeAdmin)
admin.site.register(ProfilePic, ImageAdmin)
