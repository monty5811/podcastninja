# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('podcastninja', '0003_auto_20150422_1322'),
    ]

    operations = [
        migrations.AddField(
            model_name='podcastitem',
            name='s3_url',
            field=models.TextField(blank=True, null=True, verbose_name=b'Original YT url', validators=[django.core.validators.URLValidator()]),
        ),
    ]
