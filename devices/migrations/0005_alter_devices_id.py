# Generated by Django 3.2 on 2023-08-30 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0004_alter_devices_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devices',
            name='id',
            field=models.IntegerField(editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]