# Generated by Django 4.2.4 on 2023-09-30 09:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0023_alter_unionmodel_estimated_construction_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usertokenmodel",
            name="token",
            field=models.CharField(
                default="202309-3018-2929-d4bd9f37-6f52-46ac-bcea-0da8beec19cb", max_length=255, unique=True
            ),
        ),
    ]