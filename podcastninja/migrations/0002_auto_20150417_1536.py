# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('podcastninja', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='podcastitem',
            name='url',
            field=models.TextField(verbose_name=b'Link to audio', validators=[django.core.validators.URLValidator()]),
        ),
    ]
