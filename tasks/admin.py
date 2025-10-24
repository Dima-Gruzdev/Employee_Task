from tasks.models import Task
from django.contrib import admin


class SubTaskInline(admin.TabularInline):
    model = Task
    fk_name = 'parent_task'
    extra = 0


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assignee', 'status', 'due_date')
    list_filter = ('status', 'due_date', 'assignee__department')
    search_fields = ('title', 'assignee__full_name')
    inlines = [SubTaskInline]
