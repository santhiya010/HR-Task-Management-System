from django.urls import path
from .views import MyLoginView
from . import views

urlpatterns = [
    path('hr-dashboard/', views.hr_dashboard, name='hr_dashboard'),
    path('my-tasks/', views.employee_tasks, name='employee_tasks'),
    path("create/", views.create_task, name="create_task"),
    path('complete/<int:task_id>/', views.mark_completed, name='mark_completed'),
    path("login/", MyLoginView.as_view(), name="login"),
]
