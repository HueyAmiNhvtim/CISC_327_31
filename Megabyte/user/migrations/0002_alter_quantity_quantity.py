# Generated by Django 4.2.6 on 2023-11-22 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quantity",
            name="quantity",
            field=models.PositiveIntegerField(max_length=4),
        ),
    ]