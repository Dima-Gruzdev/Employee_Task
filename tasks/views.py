from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Task
from .serializers import (BusyEmployeeSerializer,
                          ImportantTaskSuggestionSerializer, TaskSerializer)
from .services import get_busy_employees, get_important_tasks_with_suggestions


class TaskViewSet(viewsets.ModelViewSet):
    """
    Стандартный CRUD для задач.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer


@api_view(["GET"])
def busy_employees(request):
    """Возвращает список сотрудников, отсортированный по убыванию количества активных задач.

        Активными считаются задачи со статусом 'not_started' или 'in_progress'.
        Сотрудники с `is_active=False` исключаются из выборки."""

    employees = get_busy_employees()
    serializer = BusyEmployeeSerializer(employees, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def important_tasks(request):
    """Возвращает список важных задач, требующих немедленного внимания.

        Важной считается задача со статусом 'not_started', от которой зависят
        другие задачи со статусом 'in_progress'.

        Для каждой такой задачи система предлагает список сотрудников,
        подходящих для её выполнения:
          - Наименее загруженные (активных задач ≤ min + 2),
          - Приоритет — исполнитель родительской задачи (если применимо и он подходит)."""

    data = get_important_tasks_with_suggestions()
    serializer = ImportantTaskSuggestionSerializer(data, many=True)
    return Response(serializer.data)
