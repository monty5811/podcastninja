# -*- coding: utf-8 -*-
from rest_framework import serializers

from podcastninja.models import PodcastItem


class PodcastItemSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format='%d %b %H:%M')
    edit_url = serializers.CharField(source='get_edit_url')
    delete_url = serializers.CharField(source='get_del_url')

    class Meta:
        model = PodcastItem
        fields = ('title',
                  'url',
                  'description',
                  'created',
                  'edit_url',
                  'delete_url',
                  'published',
                  'failed'
                  )
