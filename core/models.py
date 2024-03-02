from django.db import models
import re
from django.core.validators import FileExtensionValidator
from .utils import ImageCompression

# Create your models here.

ALLOWED_IMAGE_EXTENSIONS = ["jpg", "jpeg", "png"]


class BaseModal(models.Model):
    """This model is Base model which will be inherited in every model..it contains the basic field needed in every model"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Company(BaseModal):
    company_id = models.CharField(max_length=555, unique=True, editable=False)
    company_name = models.CharField(max_length=25, db_index=True)
    short_code = models.CharField(max_length=8, null=True, blank=True)
    location = models.CharField(max_length=155, null=True, blank=True)
    address = models.TextField(max_length=155, null=True, blank=True)
    description = models.TextField()

    @classmethod
    def generate_company_id(cls):
        last_id = cls.objects.order_by("-id").first()
        if last_id:
            unique_id = re.search(r"\d+", last_id.company_id).group()
            unique_id = int(unique_id) + 1

        else:
            unique_id = 1001

        return f"CMP{unique_id}"

    def save(self, *args, **kwargs):
        if not self.company_id:
            self.company_id = self.generate_company_id()
        self.company_name = (
            self.company_name.capitalize() if self.company_name else None
        )
        super().save(*args, **kwargs)


class Employee(BaseModal):
    employee_id = models.CharField(max_length=555, unique=True, editable=False)
    company_id = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="employee_company"
    )
    employee_name = models.CharField(max_length=555, db_index=True)
    employee_email = models.EmailField()
    employee_mobile_number = models.CharField(max_length=12, null=True, blank=True)

    @classmethod
    def generate_company_id(cls):
        last_id = cls.objects.order_by("-id").first()
        if last_id:
            unique_id = re.search(r"\d+", last_id.employee_id).group()
            unique_id = int(unique_id) + 1
        else:
            unique_id = 1001

        return f"EMP{unique_id}"

    def save(self, *args, **kwargs):
        if not self.employee_id:
            self.employee_id = self.generate_company_id()
        self.employee_name = (
            self.employee_name.capitalize() if self.employee_name else None
        )
        super().save(*args, **kwargs)


class ProfilePic(BaseModal):
    profile_photo = models.ImageField(
        upload_to="images/",
        validators=[
            FileExtensionValidator(allowed_extensions=ALLOWED_IMAGE_EXTENSIONS)
        ],
    )

    def save(self, *args, **kwargs):
        self.profile_photo = ImageCompression.compress_image(self.profile_photo)
        super().save(*args, **kwargs)


