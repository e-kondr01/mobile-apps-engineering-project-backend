# Generated by Django 4.1.1 on 2023-05-06 15:08

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0015_remove_subject_academic_plan_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subjectinacademicplan",
            name="semesters",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.PositiveIntegerField(),
                size=None,
                verbose_name="Семестры",
            ),
        ),
    ]