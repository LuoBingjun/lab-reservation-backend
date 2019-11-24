# Generated by Django 2.2.4 on 2019-08-05 06:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20190805_0621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_secret',
            field=models.UUIDField(default=uuid.UUID('3bf694b2-b6e6-4dd6-b05d-e9df1e6ba883'), verbose_name='JWT Secret'),
        ),
    ]
