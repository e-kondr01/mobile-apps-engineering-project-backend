from rest_framework import serializers

from .models import Subject, SubjectInAcademicPlan, Task, TaskFile


class SubjectTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ("id", "title")


class TaskListSerializer(serializers.ModelSerializer):
    subject = serializers.SerializerMethodField()

    def get_subject(self, obj) -> SubjectTitleSerializer:
        return SubjectTitleSerializer(obj.subject_entry.subject).data

    class Meta:
        model = Task
        fields = ("id", "title", "subject", "deadline_at")


class TaskFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskFile
        fields = ("file",)


class TaskDetailSerializer(serializers.ModelSerializer):
    subject = serializers.SerializerMethodField()
    files = TaskFileSerializer(many=True, read_only=True)
    status = serializers.SerializerMethodField()

    def get_status(self, task: Task) -> str:
        return task.get_status(user=self.context["request"].user).value

    def get_subject(self, obj) -> SubjectTitleSerializer:
        return SubjectTitleSerializer(obj.subject_entry.subject).data

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
    subject = serializers.PrimaryKeyRelatedField(
        source="subject_entry", queryset=SubjectInAcademicPlan.objects.all()
    )

    class Meta:
        model = Task
        fields = ("id", "title", "subject", "deadline_at", "description", "links")

    # def save(self, **kwargs):
    #     print(self.validated_data)
    #     subject_entry = self.validated_data.pop("subject")
    #     self.validated_data["subject_entry"] = subject_entry
    #     return super().save(**kwargs)


class SubjectListSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="subject.title")
    teacher_name = serializers.CharField(source="subject.teacher_name")
    assessment_type = serializers.CharField(
        source="subject.get_assessment_type_display"
    )

    class Meta:
        model = SubjectInAcademicPlan
        fields = ("id", "title", "teacher_name", "assessment_type", "semesters")


class SubjectSerializer(SubjectListSerializer):
    additional_info = serializers.CharField(source="subject.additional_info")
    teacher_contacts = serializers.CharField(source="subject.teacher_contacts")

    class Meta:
        model = SubjectInAcademicPlan
        fields = (
            "id",
            "title",
            "teacher_name",
            "assessment_type",
            "additional_info",
            "teacher_contacts",
            "semesters",
        )


class UpdateSubjectSerializer(SubjectListSerializer):
    assessment_type = serializers.CharField(source="subject.assessment_type")

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
