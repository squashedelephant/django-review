# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.db import IntegrityError, models
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from simple.forms import InventoryForm, StoreForm, WidgetForm
from simple.models import Inventory, Store, Widget

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

def deleted(request, pk=None):
    context = _get_context()
    context['title'] = 'Data Deletion'
    context['pk'] = pk
    return render(request, 'simple/deleted.html', context)

def eperm(request, pk=None):
    context = _get_context()
    context['title'] = 'Permission Denied'
    context['pk'] = pk
    return render(request, 'simple/eperm.html', context)

@login_required
def home(request):
    context = _get_context()
    context['title'] = 'Simple App'
    context['user'] = request.user
    return render(request, 'simple/home.html', context)

@login_required
@cache_page(60 * 5)
def inventory_aggr(request):
    if request.method not in ['GET']:
        return Http405()
    context = _get_context()
    context['title'] = 'Simple: Total Inventory Quantities'
    template = 'simple/inventory_aggregate.html'
    try:
        inv = Inventory.objects.filter(created_by=request.user,
                                       deleted=False).aggregate(
                                       models.Sum('quantity'))
        if len(inv) > 0:
            context.update(inv)
        else:
            context['quantity_sum'] = 0
    except Inventory.DoesNotExist as e:
        context['quantity_sum'] = 0
    return render(request, template, context)
    
@login_required
@permission_required('simple.add_inventory')
def inventory_create(request):
    if request.method not in ['GET', 'POST']:
        return Http405()
    context = _get_context()
    context['title'] = 'Create a Inventory'
    template = 'simple/create_form.html'
    if request.method == 'POST':
        form = InventoryForm(data=request.POST)
        if form.is_valid():
            form.cleaned_data.update({'created_by': request.user})
            try:
                inv = Inventory(**form.cleaned_data)
                inv.save()
                inv.link = reverse_lazy('simple:inventory-detail',
                                        kwargs={'pk': inv.pk})
                inv.ulink = reverse_lazy('simple:inventory-update',
                                         kwargs={'pk': inv.pk})
                inv.dlink = reverse_lazy('simple:inventory-delete',
                                         kwargs={'pk': inv.pk})
                return HttpResponseRedirect(reverse_lazy('simple:created',
                                            kwargs={'pk': inv.pk}))
            except IntegrityError as e:
                print('ERROR: inventory_create {}'.format(str(e)))
                #err_msg = 'Name already selected, please choose another.'
                #if form.errors.has_key('name'):
                #    form.errors['name'].append(err_msg)
                #else:
                #    form.errors.update({'name': [err_msg]})
                context['form'] = form
                return render(request, template, context)
        else:
            context['form'] = form
            return render(request, template, context)
    else:
        form = InventoryForm()
        context['form'] = form
        return render(request, template, context)

@login_required
@permission_required('simple.delete_inventory')
def inventory_delete(request, pk):
    if request.method not in ['GET', 'POST']:
        return Http405()
    context = _get_context()
    context['title'] = 'Delete an Existing Inventory'
    template = 'simple/delete_form.html'
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            try:
                inv = Inventory.objects.get(created_by=request.user,
                                            pk=pk)
                inv.deleted = True
                inv.save()
                return HttpResponseRedirect(
                     reverse_lazy('simple:deleted',
                                  kwargs={'pk': pk}))
            except Inventory.DoesNotExist:
                reverse_lazy('simple:eperm',
                             kwargs={'pk': pk})
        else:
            context['form'] = form
            return render(request, template, context)
    else:
        try:
            inv = Inventory.objects.get(created_by=request.user,
                                        pk=pk)
            initial = {'created_by': request.user,
                       'name': inventory.name,
                       'cost': widget.cost}
            form = InventoryForm(initial=initial)
            context['form'] = form
            return render(request, template, context)
        except Inventory.DoesNotExist:
            reverse_lazy('simple:eperm',
                         kwargs={'pk': pk})

@login_required
@cache_page(60 * 5)
def inventory_detail(request, pk):
    if request.method not in ['GET']:
        return Http405()
    context = _get_context()
    context['title'] = 'Simple: Inventory Detail'
    template = 'simple/inventory_detail.html'
    try:
        context['inventory'] = Inventory.objects.get(created_by=request.user,
                                                     pk=pk,
                                                     deleted=False)
        return render(request, template, context)
    except Inventory.DoesNotExist as e:
        return HttpResponseRedirect(
            reverse_lazy('simple:eperm',
                         kwargs={'pk': pk}))

@login_required
@cache_page(60 * 5)
def inventory_list(request, page=0):
    if request.method not in ['GET']:
        return Http405()
    limit = 5
    offset = int(page) * limit
    limit += offset
    context = {}
    context['inventory'] = []
    context['title'] = 'Simple: Active Inventory'
    template = 'simple/inventory_list.html'
    try:
        context['inventory'] = Inventory.objects.filter(created_by=request.user,
                                                        deleted=False)[offset:limit]
        return render(request, template, context)
    except Inventory.DoesNotExist as e:
        return HttpResponseRedirect(
            reverse_lazy('simple:eperm'))
    
@login_required
@cache_page(60 * 5)
@permission_required('simple.change_inventory')
def inventory_update(request, pk):
    if request.method not in ['GET', 'POST']:
        return Http405()
    template = 'simple/update_form.html'
    context = {}
    context['title'] = 'Update an Existing Inventory'
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            try:
                # update only works on sequences
                inv = Inventory.objects.filter(created_by=request.user,
                                               pk=pk,
                                               deleted=False)
                inv.update(**form.cleaned_data)
                return HttpResponseRedirect(
                    reverse_lazy('simple:updated',
                                 kwargs={'pk': pk}))
            except Inventory.DoesNotExist:
                return HttpResponseRedirect(
                    reverse_lazy('simple:eperm',
                                 kwargs={'pk': pk}))
        else:
            context['form'] = form
            return render(request, template, context)
    else:
        try:
            inv = Inventory.objects.get(created_by=request.user, 
                                        pk=pk,
                                        deleted=False)
            initial = {'created_by': request.user,
                       'name': inv.name,
                       'cost': inv.cost}
            context['form'] = InventoryForm(initial=initial)
            return render(request, template, context)
        except Inventory.DoesNotExist:
            return HttpResponseRedirect(
                reverse_lazy('simple:eperm',
                             kwargs={'pk': pk}))

def non_existent(request, pk=None):
    context = _get_context()
    context['title'] = 'Non-Existent Object'
    context['pk'] = pk
    return render(request, 'simple/nonexistent.html', context)

@login_required
@cache_page(60 * 5)
def store_aggr(request):
    if request.method not in ['GET']:
        return Http405()
    context = _get_context()
    context['title'] = 'Simple: Total Store Quantities'
    template = 'simple/store_aggregate.html'
    try:
        context.update(Store.objects.filter(deleted=False).aggregate(
            models.Sum('quantity')))
    except Store.DoesNotExist as e:
        context['quantity_sum'] = 0
    return render(request, template, context)

@login_required
@permission_required('simple.add_store')
def store_create(request):
    if request.method not in ['GET', 'POST']:
        return Http405()
    context = _get_context()
    context['title'] = 'Create a Store'
    template = 'simple/create_form.html'
    if request.method == 'POST':
        form = StoreForm(data=request.POST)
        if form.is_valid():
            form.cleaned_data.update({'created_by': request.user})
            try:
                store = Store(**form.cleaned_data)
                store.save()
                store.link = reverse_lazy('simple:store-detail',
                                          kwargs={'pk': store.pk})
                store.ulink = reverse_lazy('simple:store-update',
                                           kwargs={'pk': store.pk})
                store.dlink = reverse_lazy('simple:store-delete',
                                           kwargs={'pk': store.pk})
                return HttpResponseRedirect(reverse_lazy('simple:created',
                                            kwargs={'pk': store.pk}))
            except IntegrityError as e:
                err_msg = 'Name already selected, please choose another.'
                if form.errors.has_key('name'):
                    form.errors['name'].append(err_msg)
                else:
                    form.errors.update({'name': [err_msg]})
                context['form'] = form
                return render(request, template, context)
        else:
            context['form'] = form
            return render(request, template, context)
    else:
        initial = {'name': 'myStore',
                   'location': 'El Cerrito'}
        context['form'] = StoreForm(initial=initial)
        return render(request, template, context)

@login_required
@permission_required('simple.delete_store')
def store_delete(request, pk):
    if request.method not in ['GET', 'POST']:
        return Http405()
    context = _get_context()
    context['title'] = 'Delete an Existing Store'
    template = 'simple/delete_form.html'
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            try:
                store = Store.objects.get(created_by=request.user,
                                          pk=pk)
                store.deleted = True
                store.save()
                return HttpResponseRedirect(
                    reverse_lazy('simple:deleted',
                                 kwargs={'pk': pk}))
            except Store.DoesNotExist:
                return HttpResponseRedirect(
                    reverse_lazy('simple:eperm',
                                 kwargs={'pk': pk}))
        else:
            context['form'] = form
            return render(request, template, context)
    else:
        store = Store.objects.get(pk=pk)
        initial = {'created_by': request.user,
                   'name': store.name,
                   'location': store.location}
        context['form'] = StoreForm(initial=initial)
    return render(request, template, context)

@login_required
@cache_page(60 * 5)
def store_detail(request, pk):
    if request.method not in ['GET']:
        return Http405()
    context = _get_context()
    context['title'] = 'Simple: Store Detail'
    template = 'simple/store_detail.html'
    try:
        context['store'] = Store.objects.get(created_by=request.user,
                                             pk=pk, 
                                             deleted=False)
        return render(request, template, context)
    except Store.DoesNotExist as e:
        return HttpResponseRedirect(
            reverse_lazy('simple:eperm',
                         kwargs={'pk': pk}))
    
@login_required
@cache_page(60 * 5)
def store_list(request, page=0):
    if request.method not in ['GET']:
        return Http405()
    limit = 5
    offset = int(page) * limit
    limit += offset
    context = {}
    context['stores'] = []
    context['title'] = 'Simple: Active Stores'
    template = 'simple/store_list.html'
    try:
        context['stores'] = Store.objects.filter(created_by=request.user,
                                                 deleted=False)[offset:limit]
        return render(request, template, context)
    except Store.DoesNotExist as e:
        return HttpResponseRedirect(
            reverse_lazy('simple:eperm'))
    
@login_required
@cache_page(60 * 5)
@permission_required('simple.change_store')
def store_update(request, pk):
    if request.method not in ['GET', 'POST']:
        return Http405()
    template = 'simple/update_form.html'
    context = {}
    context['title'] = 'Update an Existing Store'
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            try:
                # update only works on sequences
                store = Store.objects.filter(pk=pk, deleted=False)
                store.update(**form.cleaned_data)
                return HttpResponseRedirect(
                    reverse_lazy('simple:updated',
                                 kwargs={'pk': pk}))
            except Store.DoesNotExist:
                return HttpResponseRedirect(
                    reverse_lazy('simple:eperm',
                                 kwargs={'pk': pk}))
        else:
            context['form'] = form
            return render(request, template, context)
    else:
        try:
            store = Store.objects.get(pk=pk, deleted=False)
            initial = {'created_by': request.user,
                       'name': store.name,
                       'location': store.location}
            context['form'] = StoreForm(initial=initial)
            return render(request, template, context)
        except Store.DoesNotExist:
            return Http404()

@login_required
@cache_page(60 * 5)
def widget_aggr(request):
    if request.method not in ['GET']:
        return Http405()
    context = _get_context()
    context['title'] = 'Simple: Total Widget Cost'
    template = 'simple/widget_aggregate.html'
    try:
        widgets = Widget.objects.filter(created_by=request.user,
                                        deleted=False).aggregate(
                                        models.Sum('cost'))
        if len(widgets) > 0:
            context.update(widgets)
        else:
            context['cost_sum'] = 0.00
    except Widget.DoesNotExist as e:
        context['cost_sum'] = 0.00
    return render(request, template, context)
    
@login_required
@permission_required('simple.add_widget')
def widget_create(request):
    if request.method not in ['GET', 'POST']:
        return Http405()
    context = _get_context()
    context['title'] = 'Create a Widget'
    template = 'simple/create_form.html'
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
            context['form'] = form
            return render(request, template, context)
    else:
        initial = {'name': 'myWidget',
                   'sku': '111-111-11',
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
    template = 'simple/delete_form.html'
    if request.method == 'POST':
        form = WidgetForm(request.POST)
        if form.is_valid():
            try:
                widget = Widget.objects.get(created_by=request.user,
                                            pk=pk)
                widget.deleted = True
                widget.save()
                return HttpResponseRedirect(
                    reverse_lazy('simple:deleted',
                                 kwargs={'pk': pk}))
            except Widget.DoesNotExist:
                reverse_lazy('simple:eperm',
                             kwargs={'pk': pk})
        else:
            context['form'] = form
            return render(request, template, context)
    else:
        try:
            widget = Widget.objects.get(created_by=request.user,
                                        pk=pk)
            initial = {'created_by': request.user,
                       'name': widget.name,
                       'sku': widget.sku,
                       'cost': widget.cost}
            form = WidgetForm(initial=initial)
            context['form'] = form
            return render(request, template, context)
        except Widget.DoesNotExist:
            reverse_lazy('simple:eperm',
                         kwargs={'pk': pk})

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
        return render(request, template, context)
    except Widget.DoesNotExist as e:
        return HttpResponseRedirect(
            reverse_lazy('simple:eperm',
                         kwargs={'pk': pk}))

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
        widgets = Widget.objects.filter(deleted=False)[offset:limit]
        context['widgets'] = widgets
        if page > 0:
            context['prev'] = reverse_lazy('simple:widget-list',
                                           kwargs={'page': page - 1})
            context['next'] = reverse_lazy('simple:widget-list',
                                           kwargs={'page': page + 1})
        return render(request, template, context)
    except Widget.DoesNotExist as e:
        return HttpResponseRedirect(
            reverse_lazy('simple:eperm'))
    
@login_required
@cache_page(60 * 5)
@permission_required('simple.change_widget')
def widget_update(request, pk):
    if request.method not in ['GET', 'POST']:
        return Http405()
    template = 'simple/update_form.html'
    context = {}
    context['title'] = 'Update an Existing Widget'
    if request.method == 'POST':
        form = WidgetForm(request.POST)
        if form.is_valid():
            try:
                # update only works on sequences
                widget = Widget.objects.filter(pk=pk,
                                               created_by=request.user,
                                               deleted=False)
                widget.update(**form.cleaned_data)
                return HttpResponseRedirect(
                    reverse_lazy('simple:updated',
                                 kwargs={'pk': pk}))
            except Widget.DoesNotExist:
                return HttpResponseRedirect(
                    reverse_lazy('simple:eperm',
                                 kwargs={'pk': pk}))
        else:
            context['form'] = form
            return render(request, template, context)
    else:
        try:
            widget = Widget.objects.get(created_by=request.user,
                                        pk=pk,
                                        deleted=False)
            initial = {'created_by': request.user,
                       'name': widget.name,
                       'cost': widget.cost}
            context['form'] = WidgetForm(initial=initial)
            return render(request, template, context)
        except Widget.DoesNotExist:
            return HttpResponseRedirect(
                reverse_lazy('simple:eperm',
                             kwargs={'pk': pk}))

def updated(request, pk=None):
    context = _get_context()
    context['title'] = 'Data Modification'
    context['pk'] = pk
    return render(request, 'simple/updated.html', context)
