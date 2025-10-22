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
    employees = get_busy_employees()
    serializer = BusyEmployeeSerializer(employees, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def important_tasks(request):
    data = get_important_tasks_with_suggestions()
    serializer = ImportantTaskSuggestionSerializer(data, many=True)
    return Response(serializer.data)
