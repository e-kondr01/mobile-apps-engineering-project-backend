from django.contrib import admin

from .models import Subject, SubjectInAcademicPlan, Task, TaskFile


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass


@admin.register(SubjectInAcademicPlan)
class SubjectInAcademicPlanAdmin(admin.ModelAdmin):
    search_fields = ("subject__title",)


class TaskFileInline(admin.TabularInline):
    model = TaskFile


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    inlines = (TaskFileInline,)
    autocomplete_fields = ("subject_entry",)
