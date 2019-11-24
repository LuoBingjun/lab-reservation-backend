# Generated by Django 2.2.4 on 2019-08-05 06:21

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_secret',
            field=models.UUIDField(default=uuid.UUID('c554e906-3436-4f87-8c29-05e572f6a49e'), verbose_name='JWT Secret'),
        ),
    ]
