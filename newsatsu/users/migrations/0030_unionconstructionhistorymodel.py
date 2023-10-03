# Generated by Django 4.2.4 on 2023-10-03 02:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0029_usertokenmodel_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="UnionConstructionHistoryModel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255)),
                ("content", models.TextField()),
                ("union", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="users.unionmodel")),
            ],
        ),
    ]
