# Generated by Django 5.1.2 on 2025-01-12 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0002_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="in_warehouse",
        ),
    ]
