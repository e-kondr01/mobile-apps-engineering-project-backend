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
    status = serializers.SerializerMethodField()

    def get_status(self, task: Task) -> str:
        return task.get_status(user=self.context["request"].user).value

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
            "links",
            "files",
            "status",
        )


class PutTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "title", "subject", "deadline_at", "description", "links")


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ("id", "title", "teacher_info")
