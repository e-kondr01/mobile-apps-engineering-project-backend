from rest_framework import serializers

from .models import Subject, Task


class TaskListSerializer(serializers.ModelSerializer):
    subject = serializers.SlugRelatedField("title", queryset=Subject.objects.all())

    class Meta:
        model = Task
        fields = ("id", "title", "subject", "deadline_at")
