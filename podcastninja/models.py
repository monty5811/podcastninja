# -*- coding: utf-8 -*-
import logging
import uuid
from urllib.request import urlopen

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.validators import URLValidator
from django.db import models

from podcastninja import tasks

logger = logging.getLogger('podcastninja')


class PodcastItem(models.Model):
    owner = models.ForeignKey(User)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField("created",
                                   auto_now_add=True,
                                   editable=False)

    title = models.CharField("Title", max_length=100)
    description = models.TextField("Description",
                                   blank=True,
                                   null=True)
    url = models.TextField("Link to audio",
                           validators=[URLValidator()])
    s3_url = models.TextField("s3 url",
                              validators=[URLValidator()],
                              blank=True,
                              null=True)

    size = models.PositiveIntegerField()
    mime = models.CharField(max_length=100)

    published = models.BooleanField(default=True)
    failed = models.BooleanField(default=False)

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_edit_url(self):
        return reverse('edit_item', args=[str(self.uuid)])

    def get_del_url(self):
        return reverse('api_podcast_member', args=[str(self.uuid)])

    def get_audio_url(self):
        if self.s3_url is not None:
            return self.s3_url
        else:
            return self.url

    def __str__(self):
        return self.title

    @staticmethod
    def create(request, title, description, link):
        if "youtube." in link:
            p = PodcastItem.objects.create(title=title,
                                           description=description,
                                           url=link,
                                           size=0,
                                           mime='',
                                           owner=request.user,
                                           published=False,
                                           )
            tasks.convert_video.delay(url=link,
                                      uuid=str(p.uuid))

        else:
            info = urlopen(link).info()
            size = info['Content-Length']
            mime = info['Content-Type']
            p = PodcastItem.objects.create(title=title,
                                           description=description,
                                           url=link,
                                           size=size,
                                           mime=mime,
                                           owner=request.user)
        return p

    def update(self, title, description, link):
        if link == self.url:
            # no need to reprocess link
            self.title = title
            self.description = description
            self.save()
        else:
            if "youtube." in link:
                self.url = link
                self.size = 0
                self.mime = ''
                self.published = False
                self.save()
                tasks.convert_video.delay(url=self.url,
                                          uuid=str(self.uuid))
            else:
                info = urlopen(link).info()
                self.url = link
                self.size = info['Content-Length']
                self.mime = info['Content-Type']
                self.save()

    class Meta:
        ordering = ('-created',)
