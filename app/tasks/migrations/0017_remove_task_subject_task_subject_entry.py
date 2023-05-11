# Generated by Django 4.1.1 on 2023-05-06 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0016_alter_subjectinacademicplan_semesters"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="task",
            name="subject",
        ),
        migrations.AddField(
            model_name="task",
            name="subject_entry",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="tasks",
                to="tasks.subjectinacademicplan",
                verbose_name="Предмет",
            ),
        ),
    ]