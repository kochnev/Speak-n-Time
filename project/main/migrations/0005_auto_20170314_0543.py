# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-14 05:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20170312_0623'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='languages',
            new_name='language',
        ),
    ]