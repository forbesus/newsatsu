# Generated by Django 4.2.4 on 2023-09-19 01:11

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0016_alter_companyoverviewmodel_pr_text"),
    ]

    operations = [
        migrations.RenameField(
            model_name="companyachievementmodel",
            old_name="company",
            new_name="user",
        ),
    ]
