from rest_framework import serializers

from .models import Subject, Task, TaskFile


class TaskListSerializer(serializers.ModelSerializer):
    subject = serializers.SlugRelatedField("title", queryset=Subject.objects.all())

    class Meta:
        model = Task
        fields = ("id", "title", "subject", "deadline_at")


class TaskFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskFile
        fields = ("file",)


class TaskDetailSerializer(serializers.ModelSerializer):
    subject = serializers.SlugRelatedField("title", queryset=Subject.objects.all())
    files = TaskFileSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "subject",
            "deadline_at",
            "created_at",
            "updated_at",
            "description",
            "files",
        )


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ("id", "title", "teacher_info")
