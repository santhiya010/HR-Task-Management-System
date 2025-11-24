from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .models import Task
from django.contrib.auth.models import User
from .forms import TaskForm

class MyLoginView(LoginView):
    template_name = "login.html"   # your login page path
    
# -----------------------------
# HR DASHBOARD (Admin / HR)
# -----------------------------
@login_required
def hr_dashboard(request):
    # Only HR (staff member) can access
    if not request.user.is_staff:
        return redirect("employee_tasks")

    tasks = Task.objects.all()

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()
    pending_tasks = tasks.filter(completed=False).count()

    return render(request, "tasks/hr_dashboard.html", {
        "tasks": tasks,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
    })


# -----------------------------
# CREATE NEW TASK (HR ONLY)
# -----------------------------
@login_required
def create_task(request):
    if not request.user.is_staff:   # Employees should not access
        return redirect("employee_tasks")

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("hr_dashboard")
    else:
        form = TaskForm()

    return render(request, "tasks/create_task.html", {"form": form})


# -----------------------------
# EMPLOYEE TASK VIEW
# -----------------------------
@login_required
def employee_tasks(request):
    # HR should not come here — redirect HR to dashboard
    if request.user.is_staff:
        return redirect("hr_dashboard")

    tasks = Task.objects.filter(assigned_to=request.user)

    return render(request, "tasks/employee_tasks.html", {
        "tasks": tasks
    })


# -----------------------------
# MARK TASK AS COMPLETED (Employee only)
# -----------------------------
@login_required
def mark_completed(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # Employee can mark only their own task
    if task.assigned_to == request.user:
        task.completed = True
        task.save()

    return redirect("employee_tasks")
