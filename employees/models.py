from django.core.validators import MinValueValidator
from django.db import models


class Employee(models.Model):
    full_name = models.CharField(
        max_length=255,
        verbose_name="ФИО",
        help_text="Полное имя сотрудника (Фамилия Имя Отчество)",
    )
    position = models.CharField(
        max_length=255,
        verbose_name="Должность",
        help_text="Должность сотрудника в компании",
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Электронная почта",
        help_text="Корпоративная почта сотрудника",
    )
    department = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Отдел",
        help_text='Название отдела (например, "Разработка", "Маркетинг")',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
        help_text="Снимите галочку, если сотрудник уволен или в длительном отпуске",
    )
    hire_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата приёма на работу",
        help_text="Укажите дату трудоустройства",
    )
    workload_capacity = models.PositiveSmallIntegerField(
        default=5,
        validators=[MinValueValidator(1)],
        verbose_name="Макс. нагрузка",
        help_text="Максимальное количество активных задач, которые может выполнять сотрудник",
    )

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ["full_name"]

    def __str__(self):
        return f"{self.full_name} ({self.position})"
