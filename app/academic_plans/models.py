from datetime import date

from django.db import models
from django.utils import timezone


class FieldOfStudy(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")

    number = models.CharField(max_length=31, verbose_name="Код")

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Направление подготовки"
        verbose_name_plural = "Направления подготовки"


class EducationalProgram(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")

    enrollment_year = models.PositiveSmallIntegerField(
        verbose_name="Год начала обучения"
    )

    fields_of_study = models.ManyToManyField(
        to=FieldOfStudy,
        related_name="educational_programs",
        verbose_name="Направления подготовки",
    )

    @property
    def beginning_date(self):
        return date(year=int(self.enrollment_year), month=7, day=1)

    @property
    def current_semester(self):
        passed_timedelta = timezone.now().date() - self.beginning_date
        return int(passed_timedelta.days / 30 / 6 // 1 + 1)

    def __str__(self) -> str:
        return f"{self.title} {self.enrollment_year}"

    class Meta:
        verbose_name = "Образовательная программа"
        verbose_name_plural = "Образовательные программы"


class AcademicPlan(models.Model):
    educational_program = models.OneToOneField(
        to=EducationalProgram,
        on_delete=models.CASCADE,
        related_name="academic_plan",
        verbose_name="Образовательная программа",
    )

    def __str__(self) -> str:
        return f"Учебный план {self.educational_program}"

    class Meta:
        verbose_name = "Учебный план"
        verbose_name_plural = "Учебные планы"
