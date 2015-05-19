# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('podcastninja', '0004_podcastitem_s3_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='podcastitem',
            name='s3_url',
            field=models.TextField(blank=True, null=True, verbose_name=b's3 url', validators=[django.core.validators.URLValidator()]),
        ),
    ]
