from datetime import date

from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

    def validate_due_date(self, value):
        if value < date.today():
            raise serializers.ValidationError(
                "Срок оплаты не может быть перенесен в прошлое."
            )
        return value


class BusyEmployeeSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField(source='id')
    full_name = serializers.CharField()
    active_tasks_count = serializers.IntegerField()


class ImportantTaskSuggestionSerializer(serializers.Serializer):
    task_title = serializers.CharField(help_text="Название важной задачи")
    due_date = serializers.DateField(help_text="Крайний срок выполнения задания")
    suggested_employees = serializers.ListField(
        child=serializers.CharField(),
        help_text="Список полных имен сотрудников, рекомендуемых для назначения",
    )
