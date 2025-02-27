# Generated by Django 4.2.4 on 2023-08-16 08:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("constructions", "0013_alter_bidmodel_id_alter_constructionmodel_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="constructionmodel",
            name="status",
            field=models.CharField(
                choices=[
                    ("request", "見積依頼"),
                    ("question", "質問"),
                    ("answer", "応答"),
                    ("bidding", "入札"),
                    ("hearing", "ヒアリング会"),
                    ("hiring", "採用"),
                    ("evaluation", "入評価登録札"),
                ],
                default="request",
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="hearingmodel",
            name="status",
            field=models.CharField(
                choices=[("requesting", "ヒアリング会への招待中"), ("accept", "ヒアリング会承認"), ("decline", "ヒアリング会へ拒否")],
                default="requesting",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="hiremodel",
            name="status",
            field=models.CharField(
                choices=[
                    ("requesting", "採用中"),
                    ("accept", "採用承認"),
                    ("decline", "採用辞退"),
                    ("unsuccessful", "採用落選"),
                    ("finish", "作業終了"),
                    ("evaluation", "入評価登録札"),
                ],
                default="requesting",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="requestcompanymodel",
            name="status",
            field=models.CharField(
                choices=[("requesting", "見積依頼中"), ("accept", "見積依頼"), ("decline", "見積辞退"), ("unsuccessful", "落選")],
                default="requesting",
                max_length=20,
            ),
        ),
    ]
