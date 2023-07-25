# Generated by Django 4.2.2 on 2023-07-01 03:23

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='channels',
            name='type',
        ),
        migrations.RemoveField(
            model_name='devices',
            name='room',
        ),
        migrations.RemoveField(
            model_name='devices',
            name='status',
        ),
        migrations.RemoveField(
            model_name='devices',
            name='type',
        ),
        migrations.AddField(
            model_name='devices',
            name='pin',
            field=models.IntegerField(max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='channels',
            name='status',
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='devices',
            name='key',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
