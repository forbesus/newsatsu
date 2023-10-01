# Generated by Django 4.2.4 on 2023-10-01 08:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0024_alter_usertokenmodel_token"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_verify",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="usertokenmodel",
            name="token",
            field=models.CharField(
                default="202310-0117-3048-cc4ba516-8796-4ab9-b596-bae656d5ca5e", max_length=255, unique=True
            ),
        ),
    ]