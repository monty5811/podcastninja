# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from django.templatetags import static
from django.utils.feedgenerator import Rss201rev2Feed

from podcastninja.models import PodcastItem


class PNFeed(Rss201rev2Feed):
    """Podcast Ninja Feed."""
    def rss_attributes(self):
        return {'version': self._version, 'xmlns:atom': 'http://www.w3.org/2005/Atom',
                'xmlns:itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd'}

    def add_root_elements(self, handler):
        super(PNFeed, self).add_root_elements(handler)

        handler.startElement('image', {})
        handler.addQuickElement('url', self.feed['feed_image'])
        handler.addQuickElement('title', self.feed['title'])
        handler.addQuickElement('link', self.feed['link'])
        handler.endElement('image')

        handler.addQuickElement(u'itunes:image', self.feed['feed_image'])

        handler.addQuickElement('itunes:author', '')

        handler.startElement('itunes:owner', {})
        handler.addQuickElement('itunes:name', 'Podcast Ninja')
        handler.addQuickElement('itunes:email', 'pdcst.ninja@gmail.com')
        handler.endElement('itunes:owner')

        handler.addQuickElement('itunes:explicit', 'no')
        handler.addQuickElement('itunes:category', None, {'text': 'Education'})

    def add_item_elements(self, handler, item):
        super(PNFeed, self).add_item_elements(handler, item)
        handler.addQuickElement('itunes:author', '')


class PodcastFeed(Feed):
    feed_type = PNFeed
    ttl = 60

    def __init__(self):
        self.request = None

    def feed_extra_kwargs(self, obj):
        extra = {}
        extra['feed_image'] = "https://{}{}".format(self.request.get_host(), static.static('ninja.png'))
        return extra

    def get_object(self, request, username):
        self.request = request
        return get_object_or_404(User, username=username)

    def title(self, obj):
        return "{}'s Podcast Ninja Feed".format(obj.username)

    def link(self, obj):
        return "/user/{}/".format(obj.username)

    def description(self, obj):
        return "Podcast Ninja - {}.".format(obj.username)

    def items(self, obj):
        return PodcastItem.objects.filter(owner=obj).filter(published=True).filter(failed=False)[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return item.get_audio_url()

    def item_enclosure_url(self, item):
        return item.get_audio_url()

    def item_enclosure_length(self, item):
        return item.size

    def item_enclosure_mime_type(self, item):
        return item.mime

    def item_pubdate(self, item):
        return item.added
