from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"", views.TaskViewSet)

urlpatterns = [
    path('busy-employees/', views.busy_employees, name='busy-employees'),
    path('important-tasks/', views.important_tasks, name='important-tasks'),
    path("", include(router.urls)),
]
