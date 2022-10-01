from django.db import models


class Subject(models.Model):

    title = models.CharField(max_length=255, verbose_name="Название")

    # TODO: группа, преподаватель

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"


class Task(models.Model):

    title = models.CharField(max_length=255, verbose_name="Название")

    subject: Subject | None = models.ForeignKey(
        to=Subject,
        on_delete=models.CASCADE,
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

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"


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
