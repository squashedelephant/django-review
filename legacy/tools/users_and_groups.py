def get_groups():
    groups = ['view',
              'add',
              'change',
              'delete',
              'full_access']
    return groups

def get_users():
    users = {'qa': {'username': 'qa',
                    'password': 'br0k3nc0d3',
                    'email': 'qa@random.org',
                    'is_staff': True,
                    'is_superuser': False,
                    'is_active': True},
             'active': {'username': 'active',
                        'password': 'basicuser',
                        'email': 'active@random.org',
                        'is_staff': False,
                        'is_superuser': False,
                        'is_active': True},
             'staff': {'username': 'staff',
                       'password': 'adminaccess',
                       'email': 'staff@random.org',
                       'is_staff': True,
                       'is_superuser': False,
                       'is_active': True},
             'superuser': {'username': 'superuser',
                           'password': 'fullaccess',
                           'email': 'superuser@random.org',
                           'is_staff': True,
                           'is_superuser': True,
                           'is_active': True},
             'invalid': {'username': 'invalid',
                         'password': 'wrongguess',
                         'email': 'invalid@random.org',
                         'is_staff': False,
                         'is_superuser': False,
                         'is_active': False},
             'view': {'username': 'view',
                      'password': 'readonly',
                      'email': 'view@random.org',
                      'is_staff': False,
                      'is_superuser': False,
                      'is_active': True},
             'add': {'username': 'add',
                     'password': 'write',
                     'email': 'add@random.org',
                     'is_staff': False,
                     'is_superuser': False,
                     'is_active': True},
             'change': {'username': 'change',
                        'password': 'readwrite',
                        'email': 'change@random.org',
                        'is_staff': False,
                        'is_superuser': False,
                        'is_active': True},
             'delete': {'username': 'delete',
                        'password': 'write',
                        'email': 'delete@random.org',
                        'is_staff': False,
                        'is_superuser': False,
                        'is_active': True}}
    return users

def get_inventory_permissions():
    from django.contrib.auth.models import Permission
    from django.contrib.contenttypes.models import ContentType
    from simple.models import Inventory 
    content_type = ContentType.objects.get_for_model(Inventory)
    try:
        full_access = Permission.objects.get(codename='inventory.full_access')
    except Permission.DoesNotExist:
        full_access = Permission.objects.create(codename='inventory.full_access',
                                                name='User may Add, View, Change, Delete',
                                                content_type=content_type)
    add_inventory = Permission.objects.get(codename='add_inventory')
    change_inventory = Permission.objects.get(codename='change_inventory')
    delete_inventory = Permission.objects.get(codename='delete_inventory')
    permissions = {'add_inventory': add_inventory,
                   'change_inventory': change_inventory,
                   'delete_inventory': delete_inventory,
                   'full_access': full_access}
    return permissions

def get_store_permissions():
    from django.contrib.auth.models import Permission
    from django.contrib.contenttypes.models import ContentType
    from simple.models import Store
    content_type = ContentType.objects.get_for_model(Store)
    try:
        full_access = Permission.objects.get(codename='store.full_access')
    except Permission.DoesNotExist:
        full_access = Permission.objects.create(codename='store.full_access',
                                                name='User may Add, View, Change, Delete',
                                                content_type=content_type)
    add_store = Permission.objects.get(codename='add_store')
    change_store = Permission.objects.get(codename='change_store')
    delete_store = Permission.objects.get(codename='delete_store')
    permissions = {'add_store': add_store,
                   'change_store': change_store,
                   'delete_store': delete_store,
                   'full_access': full_access}
    return permissions

def get_widget_permissions():
    from django.contrib.auth.models import Permission
    from django.contrib.contenttypes.models import ContentType
    from simple.models import Widget
    content_type = ContentType.objects.get_for_model(Widget)
    try:
        full_access = Permission.objects.get(codename='widget.full_access')
    except Permission.DoesNotExist:
        full_access = Permission.objects.create(codename='widget.full_access',
                                                name='User may Add, View, Change, Delete',
                                                content_type=content_type)
    add_widget = Permission.objects.get(codename='add_widget')
    change_widget = Permission.objects.get(codename='change_widget')
    delete_widget = Permission.objects.get(codename='delete_widget')
    permissions = {'add_widget': add_widget,
                   'change_widget': change_widget,
                   'delete_widget': delete_widget,
                   'full_access': full_access}
    return permissions
