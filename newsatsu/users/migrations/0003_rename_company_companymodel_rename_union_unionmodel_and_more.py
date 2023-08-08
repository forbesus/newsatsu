# Generated by Django 4.2.4 on 2023-08-07 07:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("constructions", "0003_rename_construction_constructionmodel"),
        ("users", "0002_user_area_user_building_name_user_city_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Company",
            new_name="CompanyModel",
        ),
        migrations.RenameModel(
            old_name="Union",
            new_name="UnionModel",
        ),
        migrations.AddField(
            model_name="user",
            name="user_type",
            field=models.CharField(choices=[("管理組合", "union"), ("施工会社", "company")], default="", max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="user",
            name="name",
            field=models.CharField(blank=True, max_length=255, verbose_name="会社名"),
        ),
    ]