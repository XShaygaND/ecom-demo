# Generated by Django 5.1.2 on 2024-10-31 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Seller",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField(max_length=500)),
                ("join_date", models.DateTimeField(auto_now_add=True)),
                ("sales", models.PositiveIntegerField(default=0)),
                ("slug", models.SlugField(max_length=100, unique=True)),
                ("is_active", models.BooleanField(default=True)),
            ],
        ),
    ]
