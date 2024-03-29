# Generated by Django 4.2.2 on 2023-06-28 11:47

import core.util.model_to_dict
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=200, unique=True)),
                ('password', models.CharField(max_length=200, null=True)),
                ('role', models.IntegerField()),
            ],
            options={
                'db_table': 'User',
                'managed': True,
            },
            bases=(models.Model, core.util.model_to_dict.ModelToDictionary),
        ),
    ]
