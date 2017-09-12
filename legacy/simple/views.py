# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.db import IntegrityError, models
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from simple.forms import WidgetForm
from simple.models import Widget

class Http405(Http404):
    status_code = 405
    reason_phrase = 'FORBIDDEN'

def _get_context(context={}):
    context['header'] = 'Django: Simple App'
    context['footer'] = 'Copyright 2017 @Tim Stilwell'
    return context

def created(request, pk=None):
    context = _get_context()
    context['title'] = 'Data Submission'
    context['pk'] = pk
    return render(request, 'simple/created.html', context)

@login_required
@permission_required('simple.add_widget')
def widget_create(request):
    if request.method not in ['GET', 'POST']:
        return Http405()
    context = _get_context()
    context['title'] = 'Create a Widget'
    template = 'simple/widget_create_form.html'
    if request.method == 'POST':
        form = WidgetForm(data=request.POST)
        if form.is_valid():
            form.cleaned_data.update({'created_by': request.user})
            try:
                widget = Widget(**form.cleaned_data)
                widget.save()
                widget.link = reverse_lazy('simple:widget-detail',
                                           kwargs={'pk': widget.pk})
                widget.ulink = reverse_lazy('simple:widget-update',
                                            kwargs={'pk': widget.pk})
                widget.dlink = reverse_lazy('simple:widget-delete',
                                            kwargs={'pk': widget.pk})
                return HttpResponseRedirect(reverse_lazy('simple:created',
                                            kwargs={'pk': widget.pk}))
            except IntegrityError as e:
                err_msg = 'Name already selected, please choose another.'
                if form.errors.has_key('name'):
                    form.errors['name'].append(err_msg)
                else:
                    form.errors.update({'name': [err_msg]})
                context['form'] = form
        return render(request, template, context)
    else:
        initial = {'name': 'myWidget',
                   'cost': 0.00}
        form = WidgetForm(initial=initial)
        context['form'] = form
        return render(request, template, context)

@login_required
@permission_required('simple.delete_widget')
def widget_delete(request, pk):
    if request.method not in ['GET', 'POST']:
        return Http405()
    context = _get_context()
    context['title'] = 'Delete an Existing Widget'
    template = 'simple/widget_delete_form.html'
    if request.method == 'POST':
        context = {}
        form = WidgetForm(request.POST)
        if form.is_valid():
            try:
                widget = Widget.objects.get(pk=pk)
                widget.deleted = True
                widget.save()
            except Widget.DoesNotExist:
                pass
            return HttpResponseRedirect(
                reverse_lazy('simple:deleted',
                             kwargs={'pk': widget.pk}))
    else:
        widget = Widget.objects.get(pk=pk)
        initial = {'created_by': request.user,
                   'name': widget.name,
                   'cost': widget.cost}
        form = WidgetForm(initial=initial)
        context['form'] = form
    return render(request, template, context)

@login_required
@cache_page(60 * 5)
def widget_detail(request, pk):
    if request.method not in ['GET']:
        return Http405()
    context = _get_context()
    context['title'] = 'Simple: Widget Detail'
    template = 'simple/widget_detail.html'
    try:
        context['widget'] = Widget.objects.get(pk=pk, deleted=False)
    except Widget.DoesNotExist as e:
        pass
    return render(request, template, context)

@login_required
@cache_page(60 * 5)
def widget_list(request, page=0):
    if request.method not in ['GET']:
        return Http405()
    limit = 5
    offset = int(page) * limit
    limit += offset
    context = {}
    context['widgets'] = []
    context['title'] = 'Simple: Active Widgets'
    template = 'simple/widget_list.html'
    try:
        context['widgets'] = Widget.objects.filter(deleted=False)[offset:limit]
        return render(request, template, context)
    except Widget.DoesNotExist as e:
        return render(request, template, context)
    
@login_required
@cache_page(60 * 5)
def widget_aggr(request):
    if request.method not in ['GET']:
        return Http405()
    context = _get_context()
    context['title'] = 'Simple: Total Widget Cost'
    template = 'simple/widget_aggregate.html'
    try:
        context.update(Widget.objects.filter(deleted=False).aggregate(
            models.Sum('cost')))
    except Widget.DoesNotExist as e:
        context['cost_sum'] = 0.00
    return render(request, template, context)
    
@login_required
@cache_page(60 * 5)
@permission_required('simple.change_widget')
def widget_update(request, pk):
    if request.method not in ['GET', 'POST']:
        return Http405()
    template = 'simple/widget_update_form.html'
    context = {}
    context['title'] = 'Update an Existing Widget'
    if request.method == 'POST':
        form = WidgetForm(request.POST)
        if form.is_valid():
            try:
                # update only works on sequences
                widget = Widget.objects.filter(pk=pk, deleted=False)
                widget.update(**form.cleaned_data)
                return HttpResponseRedirect(
                    reverse_lazy('simple:updated',
                                 kwargs={'pk': widget[0].pk}))
            except Widget.DoesNotExist:
                return Http404()
    else:
        try:
            widget = Widget.objects.get(pk=pk, deleted=False)
            initial = {'created_by': request.user,
                       'name': widget.name,
                       'cost': widget.cost}
            form = WidgetForm(initial=initial)
            context['form'] = form
            return render(request, template, context)
        except Widget.DoesNotExist:
            return Http404()

def deleted(request, pk=None):
    context = _get_context()
    context['title'] = 'Data Deletion'
    context['pk'] = pk
    return render(request, 'simple/deleted.html', context)

@login_required
def home(request):
    context = _get_context()
    context['title'] = 'Simple App'
    context['user'] = request.user
    return render(request, 'simple/home.html', context)

def updated(request, pk=None):
    context = _get_context()
    context['title'] = 'Data Modification'
    context['pk'] = pk
    return render(request, 'simple/updated.html', context)
