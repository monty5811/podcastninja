# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('podcastninja', '0005_auto_20150423_1005'),
    ]

    operations = [
        migrations.AddField(
            model_name='podcastitem',
            name='added',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 23, 11, 32, 16, 283996, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='podcastitem',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 23, 11, 32, 25, 356411, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
