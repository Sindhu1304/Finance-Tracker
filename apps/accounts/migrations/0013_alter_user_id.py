# Generated by Django 5.0.1 on 2024-04-02 12:57

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(default=uuid.UUID('d8e459a9-39ea-4690-9999-f09e8248a895'), primary_key=True, serialize=False, unique=True),
        ),
    ]
