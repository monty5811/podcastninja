# -*- coding: utf-8 -*-
import logging

from allauth.account.signals import user_signed_up
from django.core.mail import send_mail
from django.dispatch import receiver

logger = logging.getLogger('podcastninja')


@receiver(user_signed_up)
def email_admin_on_signup(request, user, **kwargs):
    logger.info('New User: %s', str(user))
    send_mail("[Podcast Ninja] New User",
              "New User Signed Up!\n\nUsername: {}".format(str(user)),
              '',
              ["pdcst.ninja@gmailcom"],
              )
