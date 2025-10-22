from django.db.models import Count, Q

from employees.models import Employee

from .models import Task


def get_busy_employees():
    return (
        Employee.objects.filter(is_active=True)
        .annotate(
            active_tasks_count=Count(
                "assigned_tasks",
                filter=Q(assigned_tasks__status__in=["not_started", "in_progress"]),
            )
        )
        .order_by("-active_tasks_count")
        .only("id", "full_name")
    )


def get_important_tasks_with_suggestions():
    important_tasks = (
        Task.objects.filter(
            status=Task.Status.NOT_STARTED, subtasks__status=Task.Status.IN_PROGRESS
        )
        .distinct()
        .select_related("parent_task__assignee")
    )

    if not important_tasks.exists():
        return []

    # Получаем всех активных сотрудников с нагрузкой
    employees = (
        Employee.objects.filter(is_active=True)
        .annotate(
            active_count=Count(
                "assigned_tasks",
                filter=Q(assigned_tasks__status__in=["not_started", "in_progress"]),
            )
        )
        .only("id", "full_name")
    )

    min_active = min((emp.active_count for emp in employees), default=0)
    eligible = [emp for emp in employees if emp.active_count <= min_active + 2]
    eligible_dict = {emp.id: emp.full_name for emp in eligible}

    result = []
    for task in important_tasks:
        suggestions = []

        # Исполнитель родительской задачи, если подходит
        if task.parent_task and task.parent_task.assignee_id in eligible_dict:
            suggestions.append(eligible_dict[task.parent_task.assignee_id])

        # Остальные подходящие сотрудники
        for name in eligible_dict.values():
            if name not in suggestions:
                suggestions.append(name)

        result.append(
            {
                "task_title": task.title,
                "due_date": task.due_date,
                "suggested_employees": suggestions,
            }
        )

    return result
