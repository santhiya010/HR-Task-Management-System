from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'priority', 'due_date', 'completed')
    list_filter = ('priority', 'completed', 'due_date')
    search_fields = ('title', 'description', 'assigned_to__username')