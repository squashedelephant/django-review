# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.db import IntegrityError, models
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic import FormView, DeleteView, UpdateView

from complex.forms import EventForm, SensorForm
from complex.models import Event, Sensor 

class Http405(Http404):
    status_code = 405
    reason_phrase = 'FORBIDDEN'

def _get_context(context={}):
    context['header'] = 'Django: Complex App'
    context['footer'] = 'Copyright 2017 @Tim Stilwell'
    return context

class HomePageView(TemplateView):
    template_name = 'complex/home.html'

def home(request):
    context = _get_context()
    context['title'] = 'Complex App'
    context['user'] = request.user
    return render(request, 'complex/home.html', context)

class EventCreateView(FormView):
    template_name = 'complex/create_form.html'
    form_class = EventForm

    def form_valid(self, form):
        return super(EventCreateView, self).form_valid(form)

class EventDeleteView(FormView):
    template_name = 'complex/delete_form.html'
    form_class = EventForm
    lookup_field = 'pk'

    def form_valid(self, form):
        return super(EventDeleteView, self).form_valid(form)
    
class EventDetailView(ListView):
    template_name = 'complex/event_detail.html'
    lookup_field = 'pk'
    lookup_url_kwarg = None

class EventListView(ListView):
    template_name = 'complex/event_list.html'
    queryset = Event.objects.all()
    context_object_name = ''

class EventUpdateView(FormView):
    template_name = 'complex/update_form.html'
    form_class = EventForm
    lookup_field = 'pk'

    def form_valid(self, form):
        return super(EventUpdateView, self).form_valid(form)

class SensorCreateView(FormView):
    template_name = 'complex/create_form.html'
    form_class = SensorForm

    def form_valid(self, form):
        return super(SensorCreateView, self).form_valid(form)

class SensorDeleteView(FormView):
    template_name = 'complex/delete_form.html'
    form_class = SensorForm
    lookup_field = 'pk'

    def form_valid(self, form):
        return super(SensorDeleteView, self).form_valid(form)
    
class SensorDetailView(ListView):
    template_name = 'complex/sensor_detail.html'
    lookup_field = 'pk'
    lookup_url_kwarg = None

class SensorListView(ListView):
    template_name = 'complex/sensor_list.html'
    queryset = Sensor.objects.all()
    context_object_name = ''

class SensorUpdateView(FormView):
    template_name = 'complex/update_form.html'
    form_class = SensorForm
    lookup_field = 'pk'

    def form_valid(self, form):
        return super(SensorUpdateView, self).form_valid(form)
