from django.contrib import admin

from .models import Subject, Task, TaskFile


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass


class TaskFileInline(admin.TabularInline):
    model = TaskFile


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    inlines = (TaskFileInline,)
