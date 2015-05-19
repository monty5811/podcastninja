# -*- coding: utf-8 -*-
import pytest

from ..models import *
from ..views import *


@pytest.mark.django_db
class TestPodcastItem:

    def test_unicode(self, mp3s):
        assert str(mp3s['test_ctc1']) == 'ctc1'
        assert str(mp3s['test_example']) == 'example.com'

    def test_edit_url(self, mp3s):
        assert str(mp3s['test_ctc1'].uuid) in mp3s['test_ctc1'].get_edit_url()

    def test_del_url(self, mp3s):
        assert str(mp3s['test_ctc1'].uuid) in mp3s['test_ctc1'].get_del_url()
