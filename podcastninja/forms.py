# -*- coding: utf-8 -*-
import logging

from django import forms
from django.core.mail import send_mail
from django.forms import Textarea, TextInput

from podcastninja.models import PodcastItem

logger = logging.getLogger('podcastninja')


class NewUrlForm(forms.ModelForm):

    class Meta:
        model = PodcastItem
        exclude = ('owner',
                   'uuid',
                   'created',
                   'size',
                   'mime',
                   'published',
                   'failed',
                   's3_url',
                   )
        widgets = {
            'description': Textarea(attrs={'cols': 80,
                                           'rows': 20,
                                           'class': 'materialize-textarea'}),
            'url': TextInput(),
        }


class FeedBackForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(
        max_length=5000,
        widget=Textarea(attrs={'cols': 80,
                               'rows': 20,
                               'class': 'materialize-textarea'}),
    )

    def send_email(self, to_):
        send_mail("[Podcast Ninja] Feedback Form - {}".format(self.cleaned_data['subject']),
                  self.cleaned_data['message'],
                  '',
                  [to_],
                  )
        logger.info('New feedback. %s: %s',
                    self.cleaned_data['subject'],
                    self.cleaned_data['message'],
                    )
