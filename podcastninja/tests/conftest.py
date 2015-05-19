# -*- coding: utf-8 -*-
from urllib.request import urlopen

import pytest
from django.contrib.auth.models import User
from django.test import Client

from podcastninja.models import *


@pytest.mark.usefixtures("users")
@pytest.fixture
def mp3s(users):
    title = 'example.com'
    link = 'http://www.example.com'
    info = urlopen(link).info()
    size = info['Content-Length']
    mime = info['Content-Type']
    test_example = PodcastItem.objects.create(title=title,
                                              description='',
                                              url=link,
                                              size=size,
                                              mime=mime,
                                              owner=users['user'])

    title = 'ctc1'
    link = 'http://media.reformedforum.org/assets/download/download/audio/ctc1.mp3'
    info = urlopen(link).info()
    size = info['Content-Length']
    mime = info['Content-Type']
    test_ctc1 = PodcastItem.objects.create(title=title,
                                           description='ctc1ss',
                                           url=link,
                                           size=size,
                                           mime=mime,
                                           owner=users['user'])
    mp3s = {'test_example': test_example,
            'test_ctc1': test_ctc1,
            }
    return mp3s


@pytest.fixture
def users():
    user = User.objects.create_user(username='test',
                                    email='test@example.com',
                                    password='top_secret')
    user.save()

    c = Client()
    c.login(username='test', password='top_secret')
    c_out = Client()

    objs = {'user': user,
            'c': c,
            'c_out': c_out
            }

    return objs
