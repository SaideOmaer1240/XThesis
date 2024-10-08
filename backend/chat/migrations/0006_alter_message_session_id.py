# Generated by Django 5.0.6 on 2024-08-21 15:53

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_message_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='session_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
