# Generated by Django 4.2.4 on 2023-08-07 07:19

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_user_area_user_building_name_user_city_and_more"),
        ("constructions", "0002_alter_construction_options_construction_union"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Construction",
            new_name="ConstructionModel",
        ),
    ]
