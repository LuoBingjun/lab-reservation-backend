# Generated by Django 2.2.4 on 2019-08-05 06:34

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_remove_user_user_secret'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_secret',
            field=models.UUIDField(default=uuid.UUID('08b21503-1912-498f-9dd5-0a1b6005126f'), verbose_name='JWT Secret'),
        ),
    ]
