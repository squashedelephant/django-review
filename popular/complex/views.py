# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.paginator import InvalidPage, Paginator
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.db import IntegrityError, models
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404, render
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

def created(request, pk=None):
    context = _get_context()
    context['title'] = 'Data Submission'
    context['pk'] = pk
    return render(request, 'complex/created.html', context)

def deleted(request, pk=None):
    context = _get_context()
    context['title'] = 'Data Deletion'
    context['pk'] = pk
    return render(request, 'complex/deleted.html', context)

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
    
class EventDetailView(DetailView):
    template_name = 'complex/event_detail.html'
    lookup_field = 'pk'
    lookup_url_kwarg = None

    def get_absolute_url(self):
        return reverse_lazy('event-detail',
                            kwargs={'pk': self.pk})

class EventListView(ListView):
    form = EventForm
    template_name = 'complex/event_list.html'
    queryset = Event.objects.all()
    context_object_name = ''

class EventUpdateView(FormView):
    template_name = 'complex/update_form.html'
    form_class = EventForm
    lookup_field = 'pk'

    def form_valid(self, form):
        return super(EventUpdateView, self).form_valid(form)

class HomePageView(TemplateView):
    template_name = 'complex/index.html'

class SensorCreateView(FormView):
    template_name = 'complex/create_form.html'
    success_url = '/complex/thanks/'
    form_class = SensorForm

    def form_valid(self, form):
        #return super(SensorCreateView, self).form_valid(form)
        object = super(SensorCreateView, self).form_valid(form)
        return object

class SensorDeleteView(FormView):
    template_name = 'complex/delete_form.html'
    form_class = SensorForm
    lookup_field = 'pk'

    def form_valid(self, form):
        return super(SensorDeleteView, self).form_valid(form)
    
class SensorDetailView(DetailView):
    context_object_name = 'sensor'
    http_method_names = ['get', 'head']
    model = Sensor
    template_name = 'complex/sensor_detail.html'
    pk_url_kwarg = 'pk'

class SensorListView(ListView):
    allow_empty = True
    context_object_name = 'object_list'
    http_method_names = ['get', 'head']
    model = Sensor
    paginate_by = 5
    paginate_orphans = 0
    paginator_class = Paginator
    page_kwarg = 'page'
    template_name = 'complex/sensor_list.html'

    def get_queryset(self):
        return get_list_or_404(Sensor, created_by=self.request.user)

class SensorUpdateView(FormView):
    template_name = 'complex/update_form.html'
    form_class = SensorForm
    lookup_field = 'pk'

    def form_valid(self, form):
        return super(SensorUpdateView, self).form_valid(form)

def thanks(request):
    return render(request, 'complex/thanks.html')

def updated(request, pk=None):
    context = _get_context()
    context['title'] = 'Data Modification'
    context['pk'] = pk
    return render(request, 'complex/updated.html', context)
