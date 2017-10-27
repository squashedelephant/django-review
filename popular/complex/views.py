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

from complex.forms import EventForm, SensorForm
from complex.models import Event, Sensor 

class EventCreateView(CreateView):
    template_name = 'complex/create_form.html'
    form_class = EventForm

    def form_valid(self, form):
        return super(EventCreateView, self).form_valid(form)

class EventDeleteView(DeleteView):
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

class EventUpdateView(UpdateView):
    template_name = 'complex/update_form.html'
    form_class = EventForm
    lookup_field = 'pk'

    def form_valid(self, form):
        return super(EventUpdateView, self).form_valid(form)

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
                                        kwargs={'pk': self.object.id})
        return super(SensorCreateView, self).form_valid(form)

class SensorDeleteView(DeleteView):
    form_class = SensorForm
    http_method_not_allowed = ['delete', 'patch', 'put']
    success_url = None
    template_name = 'complex/delete_form.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.success_url = reverse_lazy('complex:deleted',
                                        kwargs={'pk': self.object.id})
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

class SensorListView(ListView):
    allow_empty = True
    context_object_name = 'object_list'
    http_method_not_allowed = ['delete', 'patch', 'post', 'put']
    model = Sensor
    paginate_by = 5
    paginate_orphans = 0
    paginator_class = Paginator
    page_kwarg = 'page'
    queryset = Sensor.objects.all()
    template_name = 'complex/sensor_list.html'

class SensorUpdateView(UpdateView):
    model = Sensor
    form_class = SensorForm
    #http_method_not_allowed = ['delete', 'patch', 'put']
    success_url = None
    template_name = 'complex/update_form.html'

    def get_form(self):
        print('kwargs: {}'.format(self.kwargs))
        if 'data' in self.kwargs:
            data = self.kwargs['data']
            del data['serial_no']
            self.kwargs.update({'instance': self.object,
                                'data': data})
        return super(SensorUpdateView, self).get_form()

    def form_valid(self, form):
        self.success_url = reverse_lazy('complex:updated',
                                        kwargs={'pk': self.object.id})
        return super(SensorUpdateView, self).form_valid(form)

    def get_initial(self):
        self.object = Sensor.objects.get(pk=self.kwargs.get('pk'))
        return {'created_by': self.request.user,
                'name': self.object.name,
                'sku': self.object.sku,
                'serial_no': self.object.serial_no.upper(),
                'camera': self.object.camera}

    def get_object(self, queryset=None):
        return Sensor.objects.get(pk=self.kwargs['pk'],
                                  created_by=self.request.user)

    #def get_queryset(self):
    #    return get_object_or_404(Sensor, 
    #                             created_by=self.request.user,
    #                             pk=self.kwargs['pk'])

class CreatedView(TemplateView):
    template_name = 'complex/created.html'

class DeletedView(TemplateView):
    template_name = 'complex/deleted.html'

class UpdatedView(TemplateView):
    template_name = 'complex/updated.html'

class ThanksView(TemplateView):
    template_name = 'complex/thanks.html'
