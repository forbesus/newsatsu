# Generated by Django 4.2.4 on 2023-09-19 01:23

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0017_rename_company_companyachievementmodel_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="companyachievementmodel",
            name="content",
        ),
    ]
