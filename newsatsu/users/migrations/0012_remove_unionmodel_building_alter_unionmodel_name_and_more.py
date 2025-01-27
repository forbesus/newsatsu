# Generated by Django 4.2.4 on 2023-08-20 23:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0011_alter_companymodel_user_alter_unionmodel_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="unionmodel",
            name="building",
        ),
        migrations.AlterField(
            model_name="unionmodel",
            name="name",
            field=models.CharField(max_length=255, verbose_name="建物名"),
        ),
        migrations.AlterField(
            model_name="user",
            name="user_type",
            field=models.CharField(choices=[("unions", "管理組合"), ("companies", "施工会社")], max_length=20),
        ),
    ]
