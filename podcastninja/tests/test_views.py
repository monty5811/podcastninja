# -*- coding: utf-8 -*-
import pytest
from django.core import mail

from ..models import *
from ..views import *


@pytest.mark.django_db
class TestStatusCodes:

    @pytest.mark.parametrize("url,status_code", [
        ("/", 200),
        ("/user/test/", 302),
        ("/feeds/test.rss", 200),
        ("/help/", 200),
        ("/about/", 200),
        ("/api/v1/items/", 403),
        ("/edit/nope/", 302),
    ])
    def test_not_logged_in(self, url, status_code, users, mp3s):
        resp = users['c_out'].get(url)
        assert resp.status_code == status_code

    @pytest.mark.parametrize("url,status_code", [
        ("/", 302),
        ("/user/test/", 200),
        ("/feeds/test.rss", 200),
        ("/help/", 200),
        ("/about/", 200),
        ("/api/v1/items/", 200),
        ("/edit/nope/", 404),
        ("/edit/", 404),
    ])
    def test_logged_in(self, url, status_code, users, mp3s):
        resp = users['c'].get(url)
        assert resp.status_code == status_code

    def test_edit_item_view(self, users, mp3s):
        resp = users['c'].get('/edit/{}/'.format(str(mp3s['test_ctc1'].uuid)))
        assert resp.status_code == 200


@pytest.mark.django_db
class TestForms:

    def test_feedback_form(self, users):
        users['c'].post('/feedback/', {'subject': 'test',
                                       'message': 'feature request'})
        assert len(mail.outbox) == 1

    def test_new_item_form(self, users):
        users['c'].post('/user/test/', {'title': 'test',
                                        'description': 'feature request',
                                        'url': 'http://www.example.com'})

    def test_bad_new_item_form(self, users):
        users['c'].post('/user/test/', {'title': 'test',
                                        'description': 'feature request',
                                        'url': 'http://www.thisisnota.tld'})

    def test_edit_item_form(self, users, mp3s):
        users['c'].post('/edit/{}/'.format(str(mp3s['test_ctc1'].uuid)),
                        {'title': mp3s['test_ctc1'].title,
                         'url': mp3s['test_ctc1'].url,
                         'description': mp3s['test_ctc1'].description,
                         })

    def test_edit_item_form_bad_link(self, users, mp3s):
        users['c'].post('/edit/{}/'.format(str(mp3s['test_ctc1'].uuid)),
                        {'title': mp3s['test_ctc1'].title,
                         'url': 'notaprotocol://nope',
                         'description': mp3s['test_ctc1'].description,
                         })


@pytest.mark.django_db
class TestAPI:

    def test_get_items(self, users, mp3s):
        resp = users['c'].get('/api/v1/items/')
        assert 'ctc' in str(resp.content)
        assert 'example' in str(resp.content)

    def test_post_new_item(self, users, mp3s):
        resp = users['c'].post('/api/v1/items/',
                               {'title': 'post test',
                                'url': 'http://example.com',
                                'description': '',
                                })
        assert 'post test' in str(resp.content)
        assert 'example' in str(resp.content)

    def test_post_new_item_no_description(self, users, mp3s):
        resp = users['c'].post('/api/v1/items/',
                               {'title': 'post test',
                                'url': 'http://example.com',
                                })
        assert 'post test' in str(resp.content)
        assert 'example' in str(resp.content)

    def test_get_item(self, users, mp3s):
        resp = users['c'].get('/api/v1/items/{}'.format(str(mp3s['test_ctc1'].uuid)))
        assert resp.status_code == 200
        assert 'ctc' in str(resp.content)

    def test_delete_item(self, users, mp3s):
        resp = users['c'].delete('/api/v1/items/{}'.format(str(mp3s['test_ctc1'].uuid)))
        assert resp.status_code == 204
        resp2 = users['c'].get('/api/v1/items/{}'.format(str(mp3s['test_ctc1'].uuid)))
        assert resp2.status_code == 404
