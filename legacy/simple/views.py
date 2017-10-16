# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.db import IntegrityError, models
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views.decorators.cache import cache_page

from simple.forms import InventoryForm, StoreForm, WidgetForm
from simple.models import Inventory, Store, Widget

class Http405(Http404):
    status_code = 405
    reason_phrase = 'FORBIDDEN'

def _get_context(context={}):
    context['header'] = 'Django: Simple App'
    context['footer'] = 'Copyright 2017 @Tim Stilwell'
    if 'prev' in context:
        del context['prev']
    if 'next' in context:
        del context['next']
    if 'aggr' in context:
        del context['aggr']
    return context

def _duplicate_key(form={}):
    keys = ['name', 'location', 'sku']
    for key in keys:
        err_msg = '{} already selected, please choose another.'
        if form.errors.has_key(key):
            form.errors[key].append(err_msg.format(key.capitalize()))
    return form

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
def inventory_aggr(request, page):
    if request.method not in ['GET']:
        return Http405()
    context = _get_context()
    context['title'] = 'Simple: Total Inventory Quantities'
    template = 'simple/inventory_aggregate.html'
    limit = settings.INVENTORIES_PER_PAGE
    offset = int(page) * limit
    limit += offset
    try:
        inv = Inventory.objects.filter(created_by=request.user,
                                       deleted=False)[offset:limit].aggregate(
                                       models.Sum('quantity'))
        context.update(inv)
    except Inventory.DoesNotExist as e:
        context['quantity_sum'] = 0
    return render(request, template, context)
    
@login_required
@permission_required('simple.add_inventory')
def inventory_create(request):
    if request.method not in ['GET', 'POST']:
        return Http405()
    context = _get_context()
    context['title'] = 'Create an Inventory'
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
                context['form'] = _duplicate_key(form)
                return render(request, template, context)
        else:
            context['form'] = form
            return render(request, template, context)
    else:
        initial = {'created_by': request.user,
                   'quantity': 1}
        form = InventoryForm(initial=initial)
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
    inventory = get_object_or_404(Inventory,
                                  pk=pk,
                                  created_by=request.user)
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        form = InventoryForm(request.POST, instance=inventory)
        if form.is_valid():
            inventory.deleted = True
            inventory.save()
            return HttpResponseRedirect(
                reverse_lazy('simple:deleted',
                             kwargs={'pk': pk}))
        else:
            context['form'] = form
            return render(request, template, context)
    else:
        inv = Inventory.objects.get(created_by=request.user,
                                    pk=pk)
        initial = {'created_by': request.user,
                   'store': inv.store,
                   'widget': inv.widget,
                   'deleted': True,
                   'quantity': inv.quantity}
        context['form'] = InventoryForm(initial=initial)
        return render(request, template, context)

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
    limit = settings.INVENTORIES_PER_PAGE
    offset = int(page) * limit
    limit += offset
    context = _get_context()
    context['title'] = 'Simple: Active Inventories'
    template = 'simple/inventory_list.html'
    inventories = get_list_or_404(Inventory,
                                  created_by=request.user,
                                  deleted=False)
    inventories = inventories[offset:limit]
    context['inventories'] = inventories
    if len(inventories) > 0:
        context['aggr'] = reverse_lazy('simple:inventory-aggr',
                                       kwargs={'page': int(page)})
    if int(page) > 0:
        context['prev'] = reverse_lazy('simple:inventory-list',
                                       kwargs={'page': int(page) - 1})
    if int(page) >= 0 and len(inventories) == settings.INVENTORIES_PER_PAGE:
        context['next'] = reverse_lazy('simple:inventory-list',
                                       kwargs={'page': int(page) + 1})
    return render(request, template, context)
    
@login_required
@cache_page(60 * 5)
@permission_required('simple.change_inventory')
def inventory_update(request, pk):
    if request.method not in ['GET', 'POST']:
        return Http405()
    template = 'simple/update_form.html'
    context = _get_context()
    context['title'] = 'Update an Existing Inventory'
    inventory = get_object_or_404(Inventory,
                                  pk=pk,
                                  created_by=request.user,
                                  deleted=False)
    if request.method == 'POST':
        form = InventoryForm(request.POST, instance=inventory)
        if form.is_valid():
            # update only works on sequences
            inventories = Inventory.objects.filter(pk=pk,
                                                   created_by=request.user,
                                                   deleted=False)
            inventories.update(**form.cleaned_data)
            return HttpResponseRedirect(
                reverse_lazy('simple:updated',
                             kwargs={'pk': pk}))
        else:
            context['form'] = form
            return render(request, template, context)
    else:
        initial = {'created_by': request.user,
                   'store': inventory.store.id,
                   'widget': inventory.widget.id}
        context['form'] = InventoryForm(initial=initial)
        return render(request, template, context)

def non_existent(request, pk=None):
    context = _get_context()
    context['title'] = 'Non-Existent Object'
    context['pk'] = pk
    return render(request, 'simple/nonexistent.html', context)

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
                context['form'] = _duplicate_key(form)
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
    store = get_object_or_404(Store,
                              pk=pk,
                              created_by=request.user)
    if request.method == 'POST':
        form = StoreForm(request.POST, instance=store)
        if form.is_valid():
            store.deleted = True
            store.save()
            return HttpResponseRedirect(
                reverse_lazy('simple:deleted',
                             kwargs={'pk': pk}))
        else:
            context['form'] = form
            return render(request, template, context)
    else:
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
    context['store'] = get_object_or_404(Store,
                                         pk=pk,
                                         created_by=request.user,
                                         deleted=False)
    return render(request, template, context)
    
@login_required
@cache_page(60 * 5)
def store_list(request, page=0):
    if request.method not in ['GET']:
        return Http405()
    limit = settings.STORES_PER_PAGE
    offset = int(page) * limit
    limit += offset
    context = _get_context()
    context['title'] = 'Simple: Active Stores'
    template = 'simple/store_list.html'
    stores = get_list_or_404(Store,
                             created_by=request.user,
                             deleted=False)
    stores = stores[offset:limit]
    context['stores'] = stores
    if int(page) > 0:
        context['prev'] = reverse_lazy('simple:store-list',
                                       kwargs={'page': int(page) - 1})
    if int(page) >= 0 and len(stores) == settings.STORES_PER_PAGE:
        context['next'] = reverse_lazy('simple:store-list',
                                       kwargs={'page': int(page) + 1})
    return render(request, template, context)
    
@login_required
@cache_page(60 * 5)
@permission_required('simple.change_store')
def store_update(request, pk):
    if request.method not in ['GET', 'POST']:
        return Http405()
    template = 'simple/update_form.html'
    context = _get_context()
    context['title'] = 'Update an Existing Store'
    store = get_object_or_404(Store,
                              pk=pk,
                              created_by=request.user,
                              deleted=False)
    if request.method == 'POST':
        form = StoreForm(request.POST, instance=store)
        if form.is_valid():
            # update only works on sequences
            stores = Store.objects.filter(pk=pk,
                                          created_by=request.user,
                                          deleted=False)
            stores.update(**form.cleaned_data)
            return HttpResponseRedirect(
                reverse_lazy('simple:updated',
                             kwargs={'pk': pk}))
        else:
            context['form'] = form
            return render(request, template, context)
    else:
        initial = {'created_by': request.user,
                   'name': store.name,
                   'location': store.location}
        context['form'] = StoreForm(initial=initial)
        return render(request, template, context)

@login_required
@cache_page(60 * 5)
def widget_aggr(request, page=0):
    if request.method not in ['GET']:
        return Http405()
    context = _get_context()
    context['title'] = 'Simple: Total Widget Cost'
    template = 'simple/widget_aggregate.html'
    limit = settings.WIDGETS_PER_PAGE
    offset = int(page) * limit
    limit += offset
    try:
        widgets = Widget.objects.filter(created_by=request.user,
                                        deleted=False)[offset:limit].aggregate(
                                        models.Sum('cost'))
        context.update(widgets)
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
                context['form'] = _duplicate_key(form)
                return render(request, template, context)
        else:
            context['form'] = form
            return render(request, template, context)
    else:
        initial = {'name': 'myWidget',
                   'sku': '111-111-11',
                   'cost': 0.00}
        context['form'] = WidgetForm(initial=initial)
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
                widget = Widget.objects.get(pk=pk,
                                            created_by=request.user)
                widget.deleted = True
                widget.save()
                return HttpResponseRedirect(
                    reverse_lazy('simple:deleted',
                                 kwargs={'pk': pk}))
            except Widget.DoesNotExist as e:
                return HttpResponseRedirect(
                    reverse_lazy('simple:non-existent',
                                 kwargs={'pk': pk}))
            except IntegrityError as e:
                context['form'] = _duplicate_key(form)
                return render(request, template, context)
        else:
            context['form'] = form
            return render(request, template, context)
    else:
        widget = Widget.objects.get(pk=pk,
                                    created_by=request.user,
                                    deleted=False)
        initial = {'created_by': request.user,
                   'name': widget.name,
                   'sku': widget.sku,
                   'cost': widget.cost}
        context['form'] = WidgetForm(initial=initial)
        return render(request, template, context)

@login_required
@cache_page(60 * 5)
def widget_detail(request, pk):
    if request.method not in ['GET']:
        return Http405()
    context = _get_context()
    context['title'] = 'Simple: Widget Detail'
    template = 'simple/widget_detail.html'
    context['widget'] = get_object_or_404(Widget,
                                          pk=pk,
                                          created_by=request.user,
                                          deleted=False)
    return render(request, template, context)

@login_required
@cache_page(60 * 5)
def widget_list(request, page=0):
    if request.method not in ['GET']:
        return Http405()
    limit = settings.WIDGETS_PER_PAGE
    offset = int(page) * limit
    limit += offset
    context = _get_context()
    context['title'] = 'Simple: Active Widgets'
    template = 'simple/widget_list.html'
    widgets = get_list_or_404(Widget,
                              deleted=False,
                              created_by=request.user)
    widgets = widgets[offset:limit]
    context['widgets'] = widgets
    if len(widgets) > 0:
        context['aggr'] = reverse_lazy('simple:widget-aggr',
                                       kwargs={'page': int(page)})
    if int(page) > 0:
        context['prev'] = reverse_lazy('simple:widget-list',
                                       kwargs={'page': int(page) - 1})
    if int(page) >= 0 and len(widgets) == settings.WIDGETS_PER_PAGE:
        context['next'] = reverse_lazy('simple:widget-list',
                                       kwargs={'page': int(page) + 1})
    return render(request, template, context)
    
@login_required
@cache_page(60 * 5)
@permission_required('simple.change_widget')
def widget_update(request, pk):
    if request.method not in ['GET', 'POST']:
        return Http405()
    template = 'simple/update_form.html'
    context = _get_context()
    context['title'] = 'Update an Existing Widget'
    if request.method == 'POST':
        form = WidgetForm(request.POST)
        if form.is_valid():
            try:
                # update only works on sequences
                widgets = Widget.objects.filter(pk=pk,
                                                created_by=request.user,
                                                deleted=False)
                widgets.update(**form.cleaned_data)
                return HttpResponseRedirect(
                    reverse_lazy('simple:updated',
                                 kwargs={'pk': pk}))
            except Widget.DoesNotExist as e:
                return HttpResponseRedirect(
                    reverse_lazy('simple:non-existent',
                                 kwargs={'pk': pk}))
            except IntegrityError as e:
                context['form'] = _duplicate_key(form)
                return render(request, template, context)
        else:
            context['form'] = form
            return render(request, template, context)
    else:
        widget = Widget.objects.get(pk=pk,
                                    created_by=request.user,
                                    deleted=False)
        initial = {'created_by': request.user,
                   'name': widget.name,
                   'cost': widget.cost}
        context['form'] = WidgetForm(initial=initial)
        return render(request, template, context)

def updated(request, pk=None):
    context = _get_context()
    context['title'] = 'Data Modification'
    context['pk'] = pk
    return render(request, 'simple/updated.html', context)
