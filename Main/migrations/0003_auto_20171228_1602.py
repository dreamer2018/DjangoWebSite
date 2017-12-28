# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0002_auto_20171201_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pictures',
            name='upvote',
            field=models.IntegerField(default=0),
        ),
    ]
