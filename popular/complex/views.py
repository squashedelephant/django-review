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
        return {'created_by': self.request.user}

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
        object = Event.objects.get(pk=self.kwargs['pk'],
                                   created_by=self.request.user)
        return object

    def get_queryset(self):
        return get_object_or_404(Event, 
                                 created_by=self.request.user,
                                 pk=self.kwargs['pk'])
    
class EventDetailView(DetailView):
    context_object_name = 'event'
    http_method_not_allowed = ['delete', 'patch', 'post', 'put']
    lookup_field = 'pk'
    model = Event
    template_name = 'complex/event_detail.html'

    def get_absolute_url(self):
        return reverse_lazy('event-detail',
                            kwargs={'pk': self.pk})

class EventListView(ListView):
    allow_empty = True
    context_object_name = 'object_list'
    http_method_not_allowed = ['delete', 'patch', 'post', 'put']
    form = EventForm
    paginate_by = 5
    paginate_orphans = 0
    paginator_class = Paginator
    page_kwarg = 'page'
    queryset = Event.objects.all()
    template_name = 'complex/event_list.html'

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

    def get_queryset(self):
        return get_object_or_404(Sensor, 
                                 created_by=self.request.user,
                                 pk=self.kwargs['pk'])

class SensorDetailView(DetailView):
    context_object_name = 'sensor'
    http_method_not_allowed = ['delete', 'patch', 'post', 'put']
    model = Sensor
    template_name = 'complex/sensor_detail.html'

    def get_absolute_url(self):
        return reverse_lazy('sensor-detail',
                            kwargs={'pk': self.pk})

class SensorListView(ListView):
    allow_empty = True
    context_object_name = 'object_list'
    form = SensorForm
    http_method_not_allowed = ['delete', 'patch', 'post', 'put']
    paginate_by = 5
    paginate_orphans = 0
    paginator_class = Paginator
    page_kwarg = 'page'
    queryset = Sensor.objects.all()
    template_name = 'complex/sensor_list.html'

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
