# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.paginator import InvalidPage, Paginator
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import IntegrityError, models
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DeleteView, DetailView
from django.views.generic import ListView, TemplateView, UpdateView

from complex.forms import EventForm, SensorForm, SensorUpdateForm
from complex.models import Event, Sensor 


class EventCreateView(CreateView):
    form_class = EventForm
    http_method_not_allowed = ['delete', 'patch', 'put']
    success_url = None
    template_name = 'complex/create_form.html'

    def get_initial(self):
        sensors = Sensor.objects.filter(created_by=self.request.user)     
        return {'sensor': sensors,
                'location': Event.LOCATIONS,
                'status': Event.STATUS,
                'camera': Event.CAMERA,
                'avg_temp': 0.00,
                'avg_pressure': 0.00,
                'pct_humidity': 0,
                'altitude': 0,
                'windspeed': 0}

    def form_valid(self, form):
        self.object = form.save()
        self.success_url = reverse_lazy('complex:created',
                                        kwargs={'pk': self.object.pk})
        return super(EventCreateView, self).form_valid(form)

class EventDeleteView(DeleteView):
    form_class = EventForm
    http_method_not_allowed = ['delete', 'patch', 'put']
    success_url = None
    template_name = 'complex/confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.success_url = reverse_lazy('complex:deleted',
                                        kwargs={'pk': self.object.pk})
        return super(EventDeleteView, self).delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        object = Event.objects.get(pk=self.kwargs['pk'])
        return object

class EventDetailView(DetailView):
    context_object_name = 'event'
    http_method_not_allowed = ['delete', 'patch', 'post', 'put']
    lookup_field = 'pk'
    model = Event
    template_name = 'complex/event_detail.html'

    def get_absolute_url(self):
        return reverse_lazy('event-detail',
                            kwargs={'pk': self.pk})

    def get_object(self, queryset=None):
        event = Event.objects.get(pk=self.kwargs['pk'])
        event.location = event.get_location_display()
        event.status = event.get_status_display()
        event.camera = event.get_camera_display()
        return event

class EventListView(ListView):
    allow_empty = True
    context_object_name = 'object_list'
    http_method_not_allowed = ['delete', 'patch', 'post', 'put']
    form = EventForm
    paginate_by = 5
    paginate_orphans = 0
    paginator_class = Paginator
    page_kwarg = 'page'
    #queryset = Event.objects.all()
    template_name = 'complex/event_list.html'

    def get_queryset(self):
        queryset = Event.objects.all()
        for event in queryset:
            event.location = event.get_location_display()
        return queryset

class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    http_method_not_allowed = ['delete', 'patch', 'put']
    success_url = None
    template_name = 'complex/update_form.html'

    def form_valid(self, form):
        form.save()
        self.success_url = reverse_lazy('complex:updated',
                                        kwargs={'pk': self.object.pk})
        return super(EventUpdateView, self).form_valid(form)

    def get_initial(self):
        return {'sensor': self.object.sensor,
                'timestamp': self.object.timestamp,
                'location': self.object.location,
                'status': self.object.status,
                'camera': self.object.camera,
                'avg_temp': self.object.avg_temp,
                'avg_pressure': self.object.avg_pressure,
                'pct_humidity': self.object.pct_humidity,
                'altitude': self.object.altitude,
                'windspeed': self.object.windspeed}

class HomePageView(TemplateView):
    template_name = 'complex/index.html'

class SensorCreateView(CreateView):
    form_class = SensorForm
    http_method_not_allowed = ['delete', 'patch', 'put']
    success_url = None
    template_name = 'complex/create_form.html'

    def get_initial(self):
        return {'created_by': self.request.user}

    def form_valid(self, form):
        self.object = form.save()
        self.success_url = reverse_lazy('complex:created',
                                        kwargs={'pk': self.object.pk})
        return super(SensorCreateView, self).form_valid(form)

class SensorDeleteView(DeleteView):
    form_class = SensorForm
    http_method_not_allowed = ['delete', 'patch', 'put']
    success_url = None
    template_name = 'complex/confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.success_url = reverse_lazy('complex:deleted',
                                        kwargs={'pk': self.object.pk})
        return super(SensorDeleteView, self).delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        object = Sensor.objects.get(pk=self.kwargs['pk'],
                                    created_by=self.request.user)
        return object

class SensorDetailView(DetailView):
    context_object_name = 'sensor'
    http_method_not_allowed = ['delete', 'patch', 'post', 'put']
    model = Sensor
    template_name = 'complex/sensor_detail.html'

    def get_absolute_url(self):
        return reverse_lazy('sensor-detail',
                            kwargs={'pk': self.pk})

    def get_object(self, queryset=None):
        sensor = Sensor.objects.get(pk=self.kwargs['pk'],
                                    created_by=self.request.user)
        sensor.temp_units = sensor.get_temp_units_display()
        sensor.pressure_units = sensor.get_pressure_units_display()
        sensor.alt_units = sensor.get_alt_units_display()
        sensor.ws_units = sensor.get_ws_units_display()
        return sensor

class SensorListView(ListView):
    allow_empty = True
    context_object_name = 'object_list'
    form = SensorForm
    http_method_not_allowed = ['delete', 'patch', 'post', 'put']
    paginate_by = 5
    paginate_orphans = 0
    paginator_class = Paginator
    page_kwarg = 'page'
    template_name = 'complex/sensor_list.html'

    def get_queryset(self):
        return get_list_or_404(Sensor,
                               created_by=self.request.user)
        print('request attrs: {}'.format(self.request.GET))
        qs = get_list_or_404(Sensor, 
                             created_by=self.request.user)
        page = self.get_paginate_by(self.request.GET.get('page'))
        return self.paginate_queryset(qs, page)
        #attrs: ['__class__', '__delattr__', '__dict__', '__doc__', '__format__',
        #        '__getattribute__', '__hash__', '__init__', '__module__', '__new__',
        #        '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__',
        #        '__str__', '__subclasshook__', '__weakref__', '_allowed_methods',
        #        'allow_empty', 'args', 'as_view', 'content_type', 'context_object_name',
        #        'dispatch', 'form', 'get', 'get_allow_empty', 'get_context_data',
        #        'get_context_object_name', 'get_ordering', 'get_paginate_by',
        #        'get_paginate_orphans', 'get_paginator', 'get_queryset', 'get_template_names',
        #        'head', 'http_method_names', 'http_method_not_allowed', 'kwargs', 'model',
        #        'options', 'ordering', 'page_kwarg', 'paginate_by', 'paginate_orphans',
        #        'paginate_queryset', 'paginator_class', 'queryset', 'render_to_response',
        #        'request', 'response_class', 'template_engine', 'template_name',
        #        'template_name_suffix']

class SensorUpdateView(UpdateView):
    model = Sensor
    form_class = SensorUpdateForm
    http_method_not_allowed = ['delete', 'patch', 'put']
    success_url = None
    template_name = 'complex/update_form.html'

    def form_valid(self, form):
        form.save()
        self.success_url = reverse_lazy('complex:updated',
                                        kwargs={'pk': self.object.id})
        return super(SensorUpdateView, self).form_valid(form)

    def get_initial(self):
        return {'created_by': self.request.user,
                'name': self.object.name,
                'sku': self.object.sku,
                'serial_no': self.object.serial_no.upper(),
                'camera': self.object.camera}

class CreatedView(TemplateView):
    template_name = 'complex/created.html'

class DeletedView(TemplateView):
    template_name = 'complex/deleted.html'

class UpdatedView(TemplateView):
    template_name = 'complex/updated.html'

class ThanksView(TemplateView):
    template_name = 'complex/thanks.html'
