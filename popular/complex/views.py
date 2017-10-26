# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.paginator import InvalidPage, Paginator
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError, models
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic import FormView, DeleteView, UpdateView

from complex.forms import EventForm, SensorForm
from complex.models import Event, Sensor 

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
    form_class = SensorForm
    success_message = 'Sensor object created successfully.'
    success_url = '/complex/thanks/'
    template_name = 'complex/create_form.html'

    def get_initial(self):
        return {'created_by': self.request.user}

    def form_valid(self, form):
        print('user: {}'.format(self.request.user.username))
        form.instance.created_by = self.request.user
        return super(SensorCreateView, self).form_valid(form)

class SensorDeleteView(DeleteView):
    form_class = SensorForm
    http_method_not_allowed = ['delete', 'patch', 'put']
    success_message = 'Sensor object deleted successfully.'
    template_name = 'complex/delete_form.html'

    def form_valid(self, form):
        return super(SensorDeleteView, self).form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super(SensorDeleteView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_queryset(self):
        qs = super(SensorDeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)

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
    template_name = 'complex/sensor_list.html'

    def get_queryset(self):
        return get_list_or_404(Sensor, created_by=self.request.user)

class SensorUpdateView(FormView):
    form_class = SensorForm
    http_method_not_allowed = ['delete', 'put']
    success_url = '/complex/thanks/'
    success_message = 'Sensor object updated successfully.'
    template_name = 'complex/update_form.html'

    def get_initial(self):
        object = Sensor.objects.get(pk=self.kwargs.get('pk'))
        return {'created_by': self.request.user,
                'name': object.name,
                'sku': object.sku,
                'serial_no': object.serial_no.upper(),
                'camera': object.camera}

    def get_object(self, queryset=None):
        object = Sensor.objects.get(pk=self.kwargs['pk'])
        return object

    def post(self, request, *args, **kwargs):
        super(SensorUpdateView, self).post(request, *args, **kwargs)

        pass

def thanks(request):
    return render(request, 'complex/thanks.html')
