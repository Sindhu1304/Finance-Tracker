# Generated by Django 5.0.1 on 2024-03-30 21:52

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(default=uuid.UUID('51f3f901-4953-4913-b56c-40e7cdb935f3'), primary_key=True, serialize=False, unique=True),
        ),
    ]
