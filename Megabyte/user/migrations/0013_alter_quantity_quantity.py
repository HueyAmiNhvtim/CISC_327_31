# Generated by Django 4.2.6 on 2023-11-02 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0012_merge_20231102_0914"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quantity",
            name="quantity",
            field=models.CharField(max_length=4),
        ),
    ]
