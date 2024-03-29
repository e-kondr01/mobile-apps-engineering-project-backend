# Generated by Django 4.1.1 on 2023-05-06 12:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("academic_plans", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="academicplan",
            name="field_of_study",
        ),
        migrations.AddField(
            model_name="educationalprogram",
            name="fields_of_study",
            field=models.ManyToManyField(
                related_name="educational_programs",
                to="academic_plans.fieldofstudy",
                verbose_name="Направления подготовки",
            ),
        ),
    ]
