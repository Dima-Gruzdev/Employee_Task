from rest_framework import serializers

from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"

    def validate_workload_capacity(self, value):
        if value < 1:
            raise serializers.ValidationError(
                "Максимальная нагрузка не может быть меньше 1."
            )
        return value
