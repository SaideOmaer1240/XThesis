# Generated by Django 5.0.6 on 2024-08-22 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_alter_message_session_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='image_path',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
