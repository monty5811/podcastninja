# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('podcastninja', '0002_auto_20150417_1536'),
    ]

    operations = [
        migrations.AddField(
            model_name='podcastitem',
            name='failed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='podcastitem',
            name='published',
            field=models.BooleanField(default=True),
        ),
    ]
