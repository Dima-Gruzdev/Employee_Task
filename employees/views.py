from rest_framework import generics

from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeListCreateView(generics.ListCreateAPIView):
    """Обрабатывает запросы к коллекции сотрудников.
        - GET /api/employees/ — возвращает список всех сотрудников."""

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Обрабатывает запросы к коллекции сотрудников.
    - GET /api/employees/{id}/ — возвращает данные сотрудника.
    - PUT /api/employees/{id}/ — полностью обновляет данные сотрудника.
    - PATCH /api/employees/{id}/ — частично обновляет данные сотрудника.
    - DELETE /api/employees/{id}/ — удаляет сотрудника."""

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
