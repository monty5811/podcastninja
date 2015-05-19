# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PodcastItem',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'created')),
                ('title', models.CharField(max_length=100, verbose_name=b'Title')),
                ('description', models.TextField(null=True, verbose_name=b'Description', blank=True)),
                ('url', models.URLField(verbose_name=b'Link to audio')),
                ('size', models.PositiveIntegerField()),
                ('mime', models.CharField(max_length=100)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
