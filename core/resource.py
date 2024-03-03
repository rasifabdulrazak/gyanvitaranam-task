from import_export import resources
from .models import Employee


class EmployeeResource(resources.ModelResource):
    class Meta:
        model = Employee
        exclude = (
            "is_active",
            "is_deleted",
            "created_at",
            "created_at",
            "updated_at",
            "employee_id",
        )

    def skip_row(self, instance, original, row, import_validation_errors=None):
        """
        This function skip rows if contains duplicate
        """
        if Employee.objects.filter(
            employee_name=instance.employee_name.lower(), company_id=instance.company_id
        ).exists():
            print(
                f"Skipped data with name '{instance.employee_name}' and company_id '{instance.company_id}'"
            )
            return True

        return False
