# Generated by Django 2.2.1 on 2019-07-06 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20190706_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='username',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
