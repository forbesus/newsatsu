# Generated by Django 4.2.4 on 2023-08-08 08:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("constructions", "0007_alter_constructionmodel_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="constructionmodel",
            name="status",
            field=models.CharField(
                choices=[
                    ("見積依頼", "request Quotation"),
                    ("質疑応答", "question and answer"),
                    ("入札", "bidding"),
                    ("ヒアリング会", "hearing party"),
                    ("採用", "hiring"),
                    ("入評価登録札", "evaluation"),
                ],
                default="見積依頼",
                max_length=30,
            ),
        ),
    ]
