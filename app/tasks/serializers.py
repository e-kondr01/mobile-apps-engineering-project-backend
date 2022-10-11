from rest_framework import serializers

from .models import Subject, Task, TaskFile


class SubjectTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ("id", "title")


class TaskListSerializer(serializers.ModelSerializer):
    subject = SubjectTitleSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ("id", "title", "subject", "deadline_at")


class TaskFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskFile
        fields = ("file",)


class TaskDetailSerializer(serializers.ModelSerializer):
    subject = SubjectTitleSerializer(read_only=True)
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


class TaskDateGroupSerializer(TaskListSerializer):
    is_urgent = serializers.BooleanField(default=False)
    is_overdue = serializers.BooleanField(default=False)

    class Meta(TaskListSerializer.Meta):
        fields = TaskListSerializer.Meta.fields + ("is_urgent", "is_overdue")


class PutTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "title", "subject", "deadline_at", "description", "links")


class SubjectSerializer(serializers.ModelSerializer):
    assessment_type = serializers.SerializerMethodField()

    def get_assessment_type(self, subject: Subject) -> str:
        return subject.get_assessment_type_display()

    class Meta:
        model = Subject
        fields = (
            "id",
            "title",
            "teacher_name",
            "assessment_type",
            "additional_info",
            "teacher_contacts",
        )


class UpdateSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = (
            "id",
            "title",
            "teacher_name",
            "assessment_type",
            "additional_info",
            "teacher_contacts",
        )


class SubjectListSerializer(serializers.ModelSerializer):
    assessment_type = serializers.SerializerMethodField()

    def get_assessment_type(self, subject: Subject) -> str:
        return subject.get_assessment_type_display()

    class Meta:
        model = Subject
        fields = ("id", "title", "teacher_name", "assessment_type")
