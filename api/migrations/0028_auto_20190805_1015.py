# Generated by Django 2.2.4 on 2019-08-05 10:15

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_auto_20190805_1015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_secret',
            field=models.UUIDField(default=uuid.UUID('749cd636-7ad3-4c3b-aea9-4763db738355'), verbose_name='JWT Secret'),
        ),
    ]
