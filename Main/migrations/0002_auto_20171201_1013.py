# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Devuser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.IntegerField()),
                ('pid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Enrolled',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('obj', models.IntegerField()),
                ('uid', models.IntegerField()),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('status', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='projects',
            name='link',
            field=models.CharField(default='https://www.baidu.com', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='projects',
            name='poster',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
