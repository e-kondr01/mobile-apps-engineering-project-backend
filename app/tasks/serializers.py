from rest_framework import serializers

from .models import Subject, Task, TaskFile


class ShortSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ("id", "title")


class TaskListSerializer(serializers.ModelSerializer):
    subject = ShortSubjectSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ("id", "title", "subject", "deadline_at")


class TaskFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskFile
        fields = ("file",)


class TaskDetailSerializer(serializers.ModelSerializer):
    subject = ShortSubjectSerializer(read_only=True)
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


class PutTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "title", "subject", "deadline_at", "description")


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ("id", "title", "teacher_info")
