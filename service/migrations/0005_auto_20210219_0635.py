# Generated by Django 3.0.2 on 2021-02-19 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_auto_20210219_0552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='mobilenum',
            field=models.IntegerField(),
        ),
    ]