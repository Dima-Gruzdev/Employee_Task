from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Employee


class EmployeeAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.employee_data = {
            "full_name": "Иванов Иван Иванович",
            "position": "Разработчик",
            "email": "ivanov@example.com",
            "department": "Backend",
            "is_active": True,
            "hire_date": "2023-01-15",
            "workload_capacity": 5
        }

    def test_create_employee(self):
        response = self.client.post(reverse('employee-list-create'), self.employee_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 1)
        self.assertEqual(Employee.objects.get().full_name, "Иванов Иван Иванович")

    def test_get_employees(self):
        Employee.objects.create(**self.employee_data)
        response = self.client.get(reverse('employee-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_employee_detail(self):
        emp = Employee.objects.create(**self.employee_data)
        response = self.client.get(reverse('employee-detail', args=[emp.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], "Иванов Иван Иванович")

    def test_update_employee(self):
        emp = Employee.objects.create(**self.employee_data)
        updated_data = {**self.employee_data, "position": "Senior Разработчик"}
        response = self.client.put(reverse('employee-detail', args=[emp.id]), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['position'], "Senior Разработчик")

    def test_delete_employee(self):
        emp = Employee.objects.create(**self.employee_data)
        response = self.client.delete(reverse('employee-detail', args=[emp.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.count(), 0)

    def test_unique_email(self):
        self.client.post(reverse('employee-list-create'), self.employee_data, format='json')
        response = self.client.post(reverse('employee-list-create'), self.employee_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
