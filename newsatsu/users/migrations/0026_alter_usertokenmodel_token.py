# Generated by Django 4.2.4 on 2023-10-01 09:18

from django.db import migrations, models
import newsatsu.users.models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0025_user_is_verify_alter_usertokenmodel_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usertokenmodel",
            name="token",
            field=models.CharField(default=newsatsu.users.models.generate_token, max_length=255, unique=True),
        ),
    ]