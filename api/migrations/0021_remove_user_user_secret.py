# Generated by Django 2.2.4 on 2019-08-05 06:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_auto_20190805_0632'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='user_secret',
        ),
    ]
