# Generated by Django 2.1 on 2018-08-19 10:22

import authentication.managers
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('object', authentication.managers.UserManager()),
            ],
        ),
    ]
