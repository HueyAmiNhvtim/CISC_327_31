# Generated by Django 4.2.6 on 2023-10-28 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0005_delete_quantity"),
    ]

    operations = [
        migrations.RenameField(
            model_name="order",
            old_name="order_id",
            new_name="user_id",
        ),
    ]
