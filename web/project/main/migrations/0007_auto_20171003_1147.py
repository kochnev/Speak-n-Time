# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-03 11:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_userprofile_video_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='code',
            field=models.CharField(max_length=3),
        ),
    ]
