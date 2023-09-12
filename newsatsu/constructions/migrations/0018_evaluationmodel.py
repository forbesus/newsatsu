# Generated by Django 4.2.4 on 2023-09-07 22:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0012_remove_unionmodel_building_alter_unionmodel_name_and_more"),
        ("constructions", "0017_alter_requestanswermodel_unique_together_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="EvaluationModel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("create_at", models.DateTimeField(auto_now_add=True)),
                ("update_at", models.DateTimeField(auto_now=True)),
                ("quality", models.FloatField(blank=True, null=True, verbose_name="品質")),
                ("correspondence", models.FloatField(blank=True, null=True, verbose_name="居住者対応")),
                ("safety", models.FloatField(blank=True, null=True, verbose_name="安全性")),
                ("period", models.FloatField(blank=True, null=True, verbose_name="工期")),
                ("maintenance", models.FloatField(blank=True, null=True, verbose_name="アフターメンテナンス")),
                ("comment", models.TextField(blank=True, null=True, verbose_name="コメント")),
                (
                    "company",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="users.companymodel"
                    ),
                ),
                (
                    "construction",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="constructions.constructionmodel"
                    ),
                ),
            ],
            options={
                "verbose_name": "工事の評価",
                "verbose_name_plural": "工事の評価",
                "unique_together": {("company", "construction")},
            },
        ),
    ]