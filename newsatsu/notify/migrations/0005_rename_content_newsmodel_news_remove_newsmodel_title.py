# Generated by Django 4.2.4 on 2023-10-03 15:26

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("notify", "0004_newsmodel"),
    ]

    operations = [
        migrations.RenameField(
            model_name="newsmodel",
            old_name="content",
            new_name="news",
        ),
        migrations.RemoveField(
            model_name="newsmodel",
            name="title",
        ),
    ]
