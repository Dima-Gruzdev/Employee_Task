from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date, timedelta
from employees.models import Employee
from tasks.models import Task


class TaskAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.employee = Employee.objects.create(
            full_name="Петров Пётр Петрович",
            position="Аналитик",
            email="petrov@example.com",
            department="Продукт",
            is_active=True,
            hire_date="2023-02-10",
            workload_capacity=4
        )
        self.task_data = {
            "title": "Написать ТЗ",
            "due_date": (date.today() + timedelta(days=5)).isoformat(),
            "status": "not_started",
            "assignee": self.employee.id
        }

    def test_create_task(self):
        response = self.client.post(reverse('task-list'), self.task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)

    def test_due_date_in_past_fails(self):
        invalid_data = {**self.task_data, "due_date": "2020-01-01"}
        response = self.client.post(reverse('task-list'), invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_tasks(self):
        Task.objects.create(
            title="Тестовая задача",
            due_date=date.today() + timedelta(days=1),
            assignee=self.employee
        )
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_task(self):
        task = Task.objects.create(
            title="Старая задача",
            due_date=date.today() + timedelta(days=2),
            assignee=self.employee
        )
        updated = {**self.task_data, "title": "Обновлённая задача"}
        response = self.client.put(reverse('task-detail', args=[task.id]), updated, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Обновлённая задача")

    def test_delete_task(self):
        task = Task.objects.create(
            title="Удаляемая задача",
            due_date=date.today() + timedelta(days=1),
            assignee=self.employee
        )
        response = self.client.delete(reverse('task-detail', args=[task.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)


class SpecialEndpointsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.emp1 = Employee.objects.create(
            full_name="Иванов И.И.",
            position="Dev",
            email="ivanov@example.com",
            workload_capacity=5
        )
        self.emp2 = Employee.objects.create(
            full_name="Петрова А.С.",
            position="QA",
            email="petrova@example.com",
            workload_capacity=3
        )

    def test_busy_employees(self):
        # Создаём 2 активные задачи для emp1
        Task.objects.create(title="Задача 1", due_date="2025-12-01", status="not_started", assignee=self.emp1)
        Task.objects.create(title="Задача 2", due_date="2025-12-02", status="in_progress", assignee=self.emp1)

        response = self.client.get(reverse('busy-employees'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['full_name'], "Иванов И.И.")
        self.assertEqual(response.data[0]['active_tasks_count'], 2)

    def test_important_tasks(self):
        # Родительская задача — NOT_STARTED
        parent = Task.objects.create(
            title="Согласовать ТЗ",
            due_date="2025-11-30",
            status="not_started"
        )
        # Дочерняя — IN_PROGRESS
        Task.objects.create(
            title="Разработать модуль",
            due_date="2025-12-10",
            status="in_progress",
            parent_task=parent,
            assignee=self.emp1
        )

        response = self.client.get(reverse('important-tasks'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['task_title'], "Согласовать ТЗ")
        self.assertIn("Иванов И.И.", response.data[0]['suggested_employees'])

    def test_important_tasks_no_results(self):
        # Нет задач с подзадачами IN_PROGRESS
        Task.objects.create(title="Обычная задача", due_date="2025-12-01", status="not_started")

        response = self.client.get(reverse('important-tasks'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
