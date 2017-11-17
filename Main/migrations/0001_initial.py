# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Anonymous',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nickname', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.IntegerField()),
                ('o_type', models.IntegerField()),
                ('obj', models.IntegerField()),
                ('content', models.TextField()),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('upvote', models.IntegerField(default=0)),
                ('deal', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('origin', models.TextField()),
                ('poster', models.CharField(max_length=255, blank=True)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('address', models.CharField(max_length=40)),
                ('labels', models.CharField(max_length=30)),
                ('reader', models.IntegerField(default=0)),
                ('upvote', models.IntegerField(default=0)),
                ('enroll', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.CharField(max_length=30)),
                ('content', models.TextField()),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('status', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('origin', models.TextField()),
                ('poster', models.CharField(max_length=255, blank=True)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('labels', models.CharField(max_length=30)),
                ('reader', models.IntegerField(default=0)),
                ('upvote', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Pictures',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=255)),
                ('link', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('upvote', models.IntegerField()),
                ('status', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('origin', models.TextField()),
                ('poster', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('reader', models.IntegerField(default=0)),
                ('upvote', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=0)),
            ],
        ),
    ]
