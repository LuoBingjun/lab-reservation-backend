# Generated by Django 2.2.4 on 2019-08-05 06:07

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20190805_0605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_secret',
            field=models.UUIDField(default=uuid.UUID('471a191e-d1db-4270-a0d7-14a465af6ce3'), verbose_name='JWT Secret'),
        ),
    ]
