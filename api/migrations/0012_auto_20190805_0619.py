# Generated by Django 2.2.4 on 2019-08-05 06:19

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20190805_0610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_secret',
            field=models.UUIDField(default=uuid.UUID('e7ad2de7-b237-49f0-8657-cad06432efb1'), verbose_name='JWT Secret'),
        ),
    ]