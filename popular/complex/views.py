# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.db import IntegrityError, models
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, TemplateView, FormView, DeleteView, UpdateView

from complex.forms import DeviceForm, MeterForm
from complex.models import Device, Meter

class Http405(Http404):
    status_code = 405
    reason_phrase = 'FORBIDDEN'

def _get_context(context={}):
    context['header'] = 'Django: Complex App'
    context['footer'] = 'Copyright 2017 @Tim Stilwell'
    return context

@login_required
def home(request):
    context = _get_context()
    context['title'] = 'Complex App'
    context['user'] = request.user
    return render(request, 'complex/home.html', context)

class DeviceCreateView(FormView):
    template_name = 'complex/device_create_form.html'
    form_class = DeviceForm

    def form_valid(self, form):
        return super(DeviceCreateView, self).form_valid(form)
    
class DeviceListView(ListView):
    template_name = 'complex/device_create_form.html'
    queryset = Device.objects.all()
    context_object_name = ''

