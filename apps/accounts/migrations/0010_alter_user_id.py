# Generated by Django 5.0.1 on 2024-04-01 09:02

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(default=uuid.UUID('0b398563-ace9-4850-8e02-2b53b9a81503'), primary_key=True, serialize=False, unique=True),
        ),
    ]
