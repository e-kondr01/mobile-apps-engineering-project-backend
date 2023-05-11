from enum import Enum

from academic_plans.models import AcademicPlan
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Case, Min, Value, When
from django.utils import timezone
from users.models import User


class Subject(models.Model):
    title = models.CharField(max_length=511, verbose_name="Название")

    teacher_name = models.CharField(
        max_length=511, blank=True, verbose_name="ФИО преподавателя"
    )

    teacher_contacts = ArrayField(
        models.CharField(max_length=127),
        blank=True,
        null=True,
        verbose_name="Контакты преподавателя",
        help_text="Несколько значений можно разделить запятой",
    )

    class AssessmentType(models.IntegerChoices):
        EXAM = 0, "Экзамен"
        CREDIT = 1, "Зачёт"
        DIFFERENTIATED_CREDIT = 2, "Дифференцированный зачёт"

    assessment_type = models.PositiveSmallIntegerField(
        choices=AssessmentType.choices,
        default=AssessmentType.CREDIT,
        verbose_name="Вид контроля",
    )

    additional_info = models.TextField(
        blank=True, verbose_name="Дополнительная информация"
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"
        ordering = ("title",)


class SubjectInAcademicPlan(models.Model):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="academic_plan_entries",
        verbose_name="Предмет",
    )

    semesters: list[int] = ArrayField(
        models.PositiveIntegerField(), verbose_name="Семестры"
    )

    academic_plan: AcademicPlan | None = models.ForeignKey(
        to=AcademicPlan,
        on_delete=models.CASCADE,
        related_name="subject_entries",
        verbose_name="Учебный план",
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return f"{self.subject} в {self.academic_plan}"

    class Meta:
        verbose_name = "Предмет в учебном плане"
        verbose_name_plural = "Предметы в учебных планах"


class Task(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")

    subject_entry: SubjectInAcademicPlan | None = models.ForeignKey(
        to=SubjectInAcademicPlan,
        on_delete=models.SET_NULL,
        related_name="tasks",
        blank=True,
        null=True,
        verbose_name="Предмет",
    )

    deadline_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Срок выполнения"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Время обновления")

    description = models.TextField(blank=True, verbose_name="Описание")

    links = models.TextField(blank=True, verbose_name="Ссылки")

    author: User | None = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        related_name="tasks",
        null=True,
        blank=True,
        verbose_name="Автор",
    )

    completed_by = models.ManyToManyField(
        to=User,
        blank=True,
        related_name="completed_tasks",
        verbose_name="Выполнено пользователями",
    )

    def __str__(self) -> str:
        task_str = self.title
        if self.subject_entry:
            task_str += ", " + str(self.subject_entry.subject)
        return task_str

    class Status(Enum):
        """
        Возможные статусы задачи для пользователя
        """

        COMPLETED = "completed"
        TODO = "todo"
        OVERDUE = "overdue"

    def get_status(self, user: User) -> Status:
        """
        Статус задачи для конкретного пользователя
        """

        if self.completed_by.filter(pk=user.pk).exists():
            return self.Status.COMPLETED

        if self.deadline_at and timezone.now() >= self.deadline_at:
            return self.Status.OVERDUE

        return self.Status.TODO

    @staticmethod
    def annotate_overdue(queryset: models.QuerySet) -> models.QuerySet:
        """
        Добавляет аннотацию к QuerySet задач в виде поля is_overdue,
        которое показывает, просрочена ли задача
        """
        queryset = queryset.annotate(
            is_overdue=Case(
                When(
                    deadline_at__lte=timezone.now(),
                    then=Value(True),
                ),
                When(
                    deadline_at__gt=timezone.now(),
                    then=Value(False),
                ),
                When(
                    deadline_at__isnull=True,
                    then=Value(False),
                ),
            ),
        )
        return queryset

    @staticmethod
    def annotate_urgent(queryset: models.QuerySet) -> models.QuerySet:
        """
        Добавляет аннотацию к QuerySet задач в виде поля is_urgent,
        которое показывает, является ли задача срочной.
        Задача является срочной, если она не выполнена, и её дедлайн
        в ближайшую дату из невыполненных задач пользователя.
        """
        urgent_date = queryset.filter(deadline_at__gt=timezone.now()).aggregate(
            Min("deadline_at__date")
        )["deadline_at__date__min"]

        queryset = queryset.annotate(
            is_urgent=Case(
                When(
                    deadline_at__date=urgent_date,
                    then=Value(True),
                ),
                When(
                    ~models.Q(deadline_at__date=urgent_date),
                    then=Value(False),
                ),
            ),
        )
        return queryset

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"
        ordering = ("deadline_at",)


class TaskFile(models.Model):
    file = models.FileField(verbose_name="Файл")

    task: Task = models.ForeignKey(
        to=Task, on_delete=models.CASCADE, related_name="files", verbose_name="Задание"
    )

    def __str__(self) -> str:
        return self.file.name

    class Meta:
        verbose_name = "Файл задания"
        verbose_name_plural = "Файлы заданий"
