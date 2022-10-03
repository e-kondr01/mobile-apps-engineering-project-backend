from django.db import models
from users.models import StudyGroup, User


class Subject(models.Model):

    title = models.CharField(max_length=255, verbose_name="Название")

    teacher_info = models.TextField(
        blank=True, verbose_name="Информация о преподавателе"
    )

    study_group: StudyGroup = models.ForeignKey(
        to=StudyGroup,
        on_delete=models.CASCADE,
        related_name="subjects",
        verbose_name="Учебная группа",
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"
        ordering = ("title",)


class Task(models.Model):

    title = models.CharField(max_length=255, verbose_name="Название")

    subject: Subject | None = models.ForeignKey(
        to=Subject,
        on_delete=models.SET_NULL,
        related_name="tasks",
        blank=True,
        null=True,
        verbose_name="Предмет",
    )

    deadline_at = models.DateField(
        null=True, blank=True, verbose_name="Срок выполнения"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Время обновления")

    description = models.TextField(blank=True, verbose_name="Описание")

    author: User | None = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        related_name="tasks",
        null=True,
        blank=True,
        verbose_name="Автор",
    )

    def __str__(self) -> str:
        task_str = self.title
        if self.subject:
            task_str += ", " + str(self.subject)
        return task_str

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
