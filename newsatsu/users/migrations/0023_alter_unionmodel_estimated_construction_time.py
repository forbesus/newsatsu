# Generated by Django 4.2.4 on 2023-09-30 04:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0022_usertokenmodel"),
    ]

    operations = [
        migrations.AlterField(
            model_name="unionmodel",
            name="estimated_construction_time",
            field=models.CharField(
                blank=True,
                max_length=7,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Year-month must be in the format 'YYYY-MM'", regex="^\\d{4}-\\d{2}$"
                    )
                ],
                verbose_name="想定工事時期",
            ),
        ),
    ]
