from academic_plans.models import AcademicPlan, EducationalProgram, FieldOfStudy
from django.contrib import admin


@admin.register(EducationalProgram)
class EducationalProgramAdmin(admin.ModelAdmin):
    pass


@admin.register(FieldOfStudy)
class FieldOfStudyAdmin(admin.ModelAdmin):
    pass


@admin.register(AcademicPlan)
class AcademicPlanAdmin(admin.ModelAdmin):
    pass
