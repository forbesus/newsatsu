# Generated by Django 4.2.4 on 2023-08-07 01:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="area",
            field=models.CharField(default="", max_length=20, verbose_name="地域"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="user",
            name="building_name",
            field=models.CharField(default="", max_length=100, verbose_name="建物名"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="user",
            name="city",
            field=models.CharField(default="", max_length=50, verbose_name="市区町村"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="user",
            name="first_name",
            field=models.CharField(blank=True, max_length=150, verbose_name="first name"),
        ),
        migrations.AddField(
            model_name="user",
            name="house_number",
            field=models.CharField(default="", max_length=20, verbose_name="番地"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="user",
            name="last_name",
            field=models.CharField(blank=True, max_length=150, verbose_name="last name"),
        ),
        migrations.AddField(
            model_name="user",
            name="post_code",
            field=models.CharField(default="", max_length=20, verbose_name="郵便番号"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="user",
            name="prefecture",
            field=models.CharField(default="", max_length=100, verbose_name="都道府県"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="user",
            name="url",
            field=models.CharField(default="", max_length=255, verbose_name="ホームページ"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="user",
            name="name",
            field=models.CharField(blank=True, max_length=255, verbose_name="User"),
        ),
        migrations.CreateModel(
            name="Union",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("building", models.CharField(max_length=255, verbose_name="建物名")),
                ("name", models.CharField(max_length=255, verbose_name="管理組合名")),
                ("total_units", models.IntegerField(verbose_name="総戸数")),
                ("floor_number", models.IntegerField(verbose_name="階数")),
                ("building_number", models.IntegerField(verbose_name="棟数")),
                (
                    "age",
                    models.IntegerField(
                        blank=True,
                        choices=[
                            (1950, 1950),
                            (1951, 1951),
                            (1952, 1952),
                            (1953, 1953),
                            (1954, 1954),
                            (1955, 1955),
                            (1956, 1956),
                            (1957, 1957),
                            (1958, 1958),
                            (1959, 1959),
                            (1960, 1960),
                            (1961, 1961),
                            (1962, 1962),
                            (1963, 1963),
                            (1964, 1964),
                            (1965, 1965),
                            (1966, 1966),
                            (1967, 1967),
                            (1968, 1968),
                            (1969, 1969),
                            (1970, 1970),
                            (1971, 1971),
                            (1972, 1972),
                            (1973, 1973),
                            (1974, 1974),
                            (1975, 1975),
                            (1976, 1976),
                            (1977, 1977),
                            (1978, 1978),
                            (1979, 1979),
                            (1980, 1980),
                            (1981, 1981),
                            (1982, 1982),
                            (1983, 1983),
                            (1984, 1984),
                            (1985, 1985),
                            (1986, 1986),
                            (1987, 1987),
                            (1988, 1988),
                            (1989, 1989),
                            (1990, 1990),
                            (1991, 1991),
                            (1992, 1992),
                            (1993, 1993),
                            (1994, 1994),
                            (1995, 1995),
                            (1996, 1996),
                            (1997, 1997),
                            (1998, 1998),
                            (1999, 1999),
                            (2000, 2000),
                            (2001, 2001),
                            (2002, 2002),
                            (2003, 2003),
                            (2004, 2004),
                            (2005, 2005),
                            (2006, 2006),
                            (2007, 2007),
                            (2008, 2008),
                            (2009, 2009),
                            (2010, 2010),
                            (2011, 2011),
                            (2012, 2012),
                            (2013, 2013),
                            (2014, 2014),
                            (2015, 2015),
                            (2016, 2016),
                            (2017, 2017),
                            (2018, 2018),
                            (2019, 2019),
                            (2020, 2020),
                            (2021, 2021),
                            (2022, 2022),
                            (2023, 2023),
                        ],
                        null=True,
                        verbose_name="築年数",
                    ),
                ),
                ("site_area", models.FloatField(blank=True, null=True, verbose_name="敷地面積")),
                ("building_area", models.FloatField(blank=True, null=True, verbose_name="建築面積")),
                ("total_floor_area", models.FloatField(blank=True, null=True, verbose_name="延床面積")),
                ("estimated_construction_time", models.DateField(blank=True, null=True, verbose_name="想定工事時期")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name": "管理組合",
                "verbose_name_plural": "管理組合",
            },
        ),
        migrations.CreateModel(
            name="Company",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("capital_stock", models.FloatField(verbose_name="資本金")),
                ("sales_amount", models.FloatField(verbose_name="売上高")),
                ("employee_number", models.IntegerField(verbose_name="社員数")),
                ("founded_year", models.DateField(verbose_name="設立年")),
                ("business_condition", models.BooleanField(verbose_name="直近3期赤字の有無")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name": "施工会社",
                "verbose_name_plural": "施工会社",
            },
        ),
    ]
