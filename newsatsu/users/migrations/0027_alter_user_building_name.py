# Generated by Django 4.2.4 on 2023-10-02 06:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0026_alter_usertokenmodel_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="building_name",
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name="建物名"),
        ),
    ]
