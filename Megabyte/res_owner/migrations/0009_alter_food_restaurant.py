# Generated by Django 4.2.6 on 2023-11-03 00:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('res_owner', '0008_alter_restaurant_location_alter_restaurant_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='res_owner.restaurant', unique=True),
        ),
    ]