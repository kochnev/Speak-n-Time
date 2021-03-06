# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-17 11:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='UserLanguage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('A1', 'Beginner'), ('A2', 'Elementary'), ('B1', 'Intermediate'), ('B2', 'Upper intermediate'), ('C1', 'Advanced'), ('C2', 'Proficient'), ('N', 'Native')], help_text='Choose your level', max_length=2)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Language')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('website', models.URLField(blank=True)),
                ('picture', models.ImageField(blank=True, upload_to='profile_images')),
                ('birthday', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('m', 'male'), ('f', 'female')], default='m', help_text='Choose your gender', max_length=1)),
                ('languages', models.ManyToManyField(help_text='Input language(e.g. english, russian, ukranian)', through='main.UserLanguage', to='main.Language')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='userlanguage',
            name='user_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.UserProfile'),
        ),
    ]
