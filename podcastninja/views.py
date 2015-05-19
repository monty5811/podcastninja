# -*- coding: utf-8 -*-
import json
import logging

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
from django.views.generic.edit import FormView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from podcastninja.forms import FeedBackForm, NewUrlForm
from podcastninja.mixins import LoginRequiredMixin
from podcastninja.models import PodcastItem

logger = logging.getLogger('podcastninja')


class RedirectHome(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(reverse('index', kwargs={'username': request.user.username}))
        else:
            return render(request, 'podcastninja/landing.html', {})


class Index(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        context = {'form': NewUrlForm}
        return render(request, 'podcastninja/index.html', context)

    def post(self, request, *args, **kwargs):
        form = NewUrlForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            link = form.cleaned_data['url']
            description = form.cleaned_data['description']
            # test url - add to db if passes, else display an error to the user
            try:
                PodcastItem.create(request, title, description, link)
                return redirect(reverse('index', kwargs={'username': request.user.username}))
            except Exception:
                form.add_error(None, 'Uh, oh, something went wrong with that link')
                logger.warning('Adding a link failed',
                               exc_info=True,
                               extra={'url': str(link),
                                      'user': str(request.user),
                                      }
                               )

        context = {'form': form}

        return render(request, 'podcastninja/index.html', context)


class EditLink(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        try:
            pitem = get_object_or_404(PodcastItem, uuid=kwargs['uuid'])
            context = {'form': NewUrlForm(instance=pitem)}
            return render(request, 'podcastninja/edit.html', context)
        except KeyError:
            return redirect(reverse('index', kwargs={'username': request.user.username}))
        except ValueError:
            raise Http404("Item does not exist")

    def post(self, request, *args, **kwargs):
        form = NewUrlForm(request.POST)
        if form.is_valid():
            pitem = get_object_or_404(PodcastItem, uuid=kwargs['uuid'])
            # test url - add to db if passes, else display an error to the user
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            link = form.cleaned_data['url']
            try:
                pitem.update(title, description, link)
                return redirect(reverse('index', kwargs={'username': request.user.username}))
            except Exception:
                form.add_error(None, 'Uh, oh, something went wrong with that link')
                logger.warning('Adding a link failed',
                               exc_info=True,
                               extra={'url': str(link),
                                      'user': str(request.user),
                                      }
                               )

        context = {'form': form}

        return render(request, 'podcastninja/index.html', context)


class FeedbackView(FormView):
    template_name = 'podcastninja/contact.html'
    form_class = FeedBackForm
    success_url = '/'

    def form_valid(self, form):
        form.send_email("pdcst.ninja@gmailcom")
        messages.add_message(self.request, messages.INFO, 'Thanks for your feedback!')
        return super(FeedbackView, self).form_valid(form)


class ApiCollection(APIView):
    model_class = None
    serializer_class = None

    def get(self, request, format=None):
        objs = self.model_class.objects.filter(owner=request.user)
        serializer = self.serializer_class(objs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        title = request.data['title']
        description = request.data.get('description', '')
        link = request.data['url']
        try:
            p = PodcastItem.create(request, title, description, link)
            serializer = self.serializer_class(p)
            return Response(serializer.data)
        except Exception:
            return HttpResponse(
                json.dumps({'title': title,
                            'url': link,
                            'error': 'Uh, oh, something went wrong with that link'
                            }),
                content_type="application/json"
            )


class ApiMember(APIView):
    model_class = None
    serializer_class = None

    def get(self, request, format=None, **kwargs):
        obj = get_object_or_404(self.model_class, uuid=kwargs['uuid'])
        serializer = self.serializer_class(obj)
        return Response(serializer.data)

    def delete(self, request, format=None, **kwargs):
        obj = get_object_or_404(self.model_class, uuid=kwargs['uuid'])
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
