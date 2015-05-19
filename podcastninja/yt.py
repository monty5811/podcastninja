# -*- coding: utf-8 -*-
import logging
import os
from urllib.request import urlopen

import boto
import youtube_dl
from django.conf import settings

logger = logging.getLogger('podcastninja')


class YtLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        logger.warning('[YoutubeDL] %s', msg)

    def error(self, msg):
        logger.error('[YoutubeDL] %s', msg)


class YoutubeVideo(object):
    """
    Convert a Youtube video to mp3 and upload to S3.
    Uses youtube-dl

    ## Steps

    1. Call youtube-dl and have it use ffmpeg to produce an mp3
    2. Use call back hook to find the mp3 filename
    3. Send the file to amazon s3. Filename is the link's uuid
    4. Mark link as published
    5. Delete tmp file

    ## TODO
    - Improve reliability
    """
    def __init__(self, url, uuid):
        super(YoutubeVideo, self).__init__()
        self.url = url
        self.uuid = uuid
        self.output_filename = ''

    def yt2mp3(self):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '96',
            }],
            'logger': YtLogger(),
            'progress_hooks': [self.extract_filename],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])
        self.send2s3()

    def extract_filename(self, d):
        if d['status'] == 'finished':
            filename = d['filename']
            filename = filename[:filename.rfind('.')]
            filename += '.mp3'
            self.output_filename = filename

    def send2s3(self):
        from podcastninja.models import PodcastItem
        p = PodcastItem.objects.get(uuid=self.uuid)
        try:
            sourcepath = self.output_filename

            bucket_name = settings.AWS_BUCKET
            conn = boto.connect_s3(settings.AWS_ACCESS_KEY_ID, settings.AWS_ACCESS_KEY_SECRET)
            bucket = conn.get_bucket(bucket_name)

            k = boto.s3.key.Key(bucket)
            k.key = self.uuid
            logger.info('Begin upload of %s to S3', sourcepath)
            k.set_contents_from_filename(sourcepath)
            logger.info('End upload of %s to S3', sourcepath)
            k.set_canned_acl('public-read')
            url = k.generate_url(expires_in=0, query_auth=False)

            # add url to db and turn on "published" flag
            p.s3_url = url
            info = urlopen(url).info()
            p.size = info['Content-Length']
            p.mime = info['Content-Type']
            p.published = True
            p.failed = False
            p.save()

            # remove file
            os.remove(sourcepath)
            logger.info('Delete tmp file: %s', sourcepath)
        except Exception:
            logger.error('Youtube link error',
                         exc_info=True,
                         extra={'uuid': str(self.uuid)}
                         )
            p.failed = True
