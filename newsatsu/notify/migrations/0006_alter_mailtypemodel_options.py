# Generated by Django 4.2.4 on 2023-10-06 08:26

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("notify", "0005_rename_content_newsmodel_news_remove_newsmodel_title"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="mailtypemodel",
            options={"verbose_name": "メールテンプレートID", "verbose_name_plural": "メールテンプレートID"},
        ),
    ]