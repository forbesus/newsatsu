# Generated by Django 4.2.4 on 2023-09-29 09:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("notify", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="MailTypeModel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("label", models.CharField(max_length=50, unique=True)),
                ("template_id", models.CharField(blank=True, max_length=50)),
                ("description", models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.AlterModelOptions(
            name="notificationmodel",
            options={"verbose_name": "お知らせ", "verbose_name_plural": "お知らせ"},
        ),
        migrations.AddField(
            model_name="notificationmodel",
            name="template_id",
            field=models.CharField(default="", max_length=50),
            preserve_default=False,
        ),
    ]