# Generated by Django 4.2.4 on 2023-09-18 15:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0015_alter_companyachievementmodel_company_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="companyoverviewmodel",
            name="pr_text",
            field=models.TextField(blank=True, null=True),
        ),
    ]
