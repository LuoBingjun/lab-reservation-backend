# Generated by Django 2.2.1 on 2019-08-05 02:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20190805_0249'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='onlinetoken',
            name='user',
        ),
        migrations.DeleteModel(
            name='Account',
        ),
        migrations.DeleteModel(
            name='OnlineToken',
        ),
    ]
