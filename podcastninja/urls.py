# -*- coding: utf-8 -*-
from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.views.generic.base import TemplateView

import podcastninja.signals  # pragma: no flakes
from podcastninja.feeds import PodcastFeed
from podcastninja.models import PodcastItem
from podcastninja.serializers import PodcastItemSerializer
from podcastninja.views import (ApiCollection, ApiMember, EditLink,
                                FeedbackView, Index, RedirectHome)

admin.autodiscover()
urlpatterns = patterns('',
                       url(r'^admin-panel/', include(admin.site.urls)),
                       url(r'^accounts/', include('allauth.urls')),
                       # add rss url
                       url(r'^feeds/(?P<username>\w+).rss', PodcastFeed(), name='feed'),
                       url(r'^edit/(?P<uuid>[^/]+)/', EditLink.as_view(), name='edit_item'),
                       url(r'^feedback/', FeedbackView.as_view(), name='feedback'),
                       url(r'^help/', TemplateView.as_view(template_name='podcastninja/help.html'), name='help'),
                       url(r'^about/', TemplateView.as_view(template_name='podcastninja/about.html'), name='about'),
                       # add rest urls
                       url(r'^api/v1/items/$',
                           ApiCollection.as_view(model_class=PodcastItem,
                                                 serializer_class=PodcastItemSerializer),
                           name='api_podcast_collection'),
                       url(r'^api/v1/items/(?P<uuid>[^/]+)$',
                           ApiMember.as_view(model_class=PodcastItem,
                                             serializer_class=PodcastItemSerializer),
                           name='api_podcast_member'),
                       # add form url
                       url(r'^user/(?P<username>\w+)/$', Index.as_view(), name='index'),
                       url(r'^$', RedirectHome.as_view(), name='index')
                       )
