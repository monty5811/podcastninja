# -*- coding: utf-8 -*-
from celery import shared_task

from podcastninja.yt import YoutubeVideo


@shared_task()
def convert_video(url, uuid):
    y = YoutubeVideo(url=url.replace('https://', 'http://'),
                     uuid=uuid)
    y.yt2mp3()
