# Generated by Django 5.0.1 on 2024-04-03 20:38

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(default=uuid.UUID('8b1e0360-7b22-4a58-ac39-f0a480a48ba2'), primary_key=True, serialize=False, unique=True),
        ),
    ]
