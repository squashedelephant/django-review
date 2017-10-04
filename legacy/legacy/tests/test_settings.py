
from django.conf import settings
from django.test import TestCase

class TestSettings(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_01_base_dir(self):
        self.assertTrue(settings.is_overridden('ALLOWED_HOSTS'))
        self.assertEquals(list, type(settings.ALLOWED_HOSTS))
        self.assertListEqual(['127.0.0.1', 'testserver'], settings.ALLOWED_HOSTS)

    def test_02_auth_password_validators(self):
        validators = [{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
                      {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
                      {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'}, 
                      {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}]
        self.assertTrue(settings.is_overridden('AUTH_PASSWORD_VALIDATORS'))
        self.assertEquals(list, type(settings.AUTH_PASSWORD_VALIDATORS))
        self.assertEquals(validators, settings.AUTH_PASSWORD_VALIDATORS) 


    def test_03_base_dir(self):
        self.assertTrue(settings.is_overridden('BASE_DIR'))
        self.assertEquals(str, type(settings.BASE_DIR))
        self.assertEquals('/Users/tim/Project/django-review/legacy/legacy', settings.BASE_DIR) 
    
    def test_04_databases(self):
        databases = {'default': {'ATOMIC_REQUESTS': False,
                                 'AUTOCOMMIT': True,
                                 'CONN_MAX_AGE': 0,
                                 'ENGINE': 'django.db.backends.sqlite3',
                                 'HOST': '',
                                 'NAME': ':memory:',
                                 'OPTIONS': {},
                                 'PASSWORD': '',
                                 'PORT': '',
                                 'TEST': {'CHARSET': None,
                                 'COLLATION': None,
                                 'MIRROR': None,
                                 'NAME': None},
                                 'TIME_ZONE': None,
                                 'USER': ''}}
        self.assertTrue(settings.is_overridden('DATABASES'))
        self.assertEquals(dict, type(settings.DATABASES))
        self.assertDictEqual(databases, settings.DATABASES)

    def test_05_debug(self):
        self.assertTrue(settings.is_overridden('DEBUG'))
        self.assertEquals(bool, type(settings.DEBUG))
        self.assertFalse(settings.DEBUG) 
    
    def test_06_fixture_dirs(self):
        self.assertTrue(settings.is_overridden('FIXTURE_DIRS'))
        self.assertEquals(tuple, type(settings.FIXTURE_DIRS))
        self.assertTupleEqual(('/Users/tim/Project/django-review/legacy/legacy/fixtures',), settings.FIXTURE_DIRS) 
    
    def test_07_installed_apps(self):
        installed_apps = ['django.contrib.admin',
                          'django.contrib.auth',
                          'django.contrib.contenttypes',
                          'django.contrib.sessions',
                          'django.contrib.messages',
                          'django.contrib.staticfiles',
                          'simple']
        self.assertTrue(settings.is_overridden('INSTALLED_APPS'))
        self.assertEquals(list, type(settings.INSTALLED_APPS))
        self.assertListEqual(installed_apps, settings.INSTALLED_APPS) 
    
    def test_08_language_code(self):
        self.assertTrue(settings.is_overridden('LANGUAGE_CODE'))
        self.assertEquals(str, type(settings.LANGUAGE_CODE))
        self.assertEquals('en-us', settings.LANGUAGE_CODE) 
    
    def test_09_login_url(self):
        self.assertTrue(settings.is_overridden('LOGIN_URL'))
        self.assertEquals(str, type(settings.LOGIN_URL))
        self.assertEquals('/login/', settings.LOGIN_URL) 
    
    def test_10_middleware(self):
        middleware = ['django.middleware.security.SecurityMiddleware',
                      'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.middleware.common.CommonMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware',
                      'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware',
                      'django.middleware.clickjacking.XFrameOptionsMiddleware']
        self.assertTrue(settings.is_overridden('MIDDLEWARE'))
        self.assertEquals(list, type(settings.MIDDLEWARE))
        self.assertListEqual(middleware, settings.MIDDLEWARE) 
    
    def test_11_nose_args(self):
        nose_args = ['--verbosity=2',
                     '--with-coverage',
                     '--cover-package=legacy,simple',
                     '--cover-erase',
                     '--cover-branches',
                     '--cover-html',
                     '--cover-html-dir=results',
                     '--cover-min-percentage=80']
        self.assertTrue(settings.is_overridden('NOSE_ARGS'))
        self.assertEquals(list, type(settings.NOSE_ARGS))
        self.assertListEqual(nose_args, settings.NOSE_ARGS) 
    
    def test_12_nose_cover_branches(self):
        nose_cover_branches = ['develop']
        self.assertTrue(settings.is_overridden('NOSE_COVER_BRANCHES'))
        self.assertEquals(list, type(settings.NOSE_COVER_BRANCHES))
        self.assertListEqual(nose_cover_branches, settings.NOSE_COVER_BRANCHES) 
    
    def test_13_project_root(self):
        self.assertTrue(settings.is_overridden('PROJECT_ROOT'))
        self.assertEquals(str, type(settings.PROJECT_ROOT))
        self.assertEquals('/Users/tim/Project/django-review/legacy/legacy', settings.PROJECT_ROOT) 
    
    def test_14_root_urlconf(self):
        self.assertTrue(settings.is_overridden('ROOT_URLCONF'))
        self.assertEquals(str, type(settings.ROOT_URLCONF))
        self.assertEquals('legacy.urls', settings.ROOT_URLCONF) 
    
    def test_15_secret_key(self):
        self.assertTrue(settings.is_overridden('SECRET_KEY'))
        self.assertEquals(str, type(settings.SECRET_KEY))
        self.assertEquals('qhea@8(uu_zj_7$pg369o_v+f5h3y31vet2z*brq#1+v0@+*h_', settings.SECRET_KEY) 
    
    def test_16_staticfiles_dirs(self):
        staticfiles_dirs = ('/Users/tim/Project/django-review/legacy/legacy/static',)
        self.assertTrue(settings.is_overridden('STATICFILES_DIRS'))
        self.assertEquals(tuple, type(settings.STATICFILES_DIRS))
        self.assertTupleEqual(staticfiles_dirs, settings.STATICFILES_DIRS) 
    
    def test_17_static_root(self):
        self.assertTrue(settings.is_overridden('STATIC_ROOT'))
        self.assertEquals(str, type(settings.STATIC_ROOT))
        self.assertEquals('/Users/tim/Project/django-review/legacy/legacy/staticfiles', settings.STATIC_ROOT) 
    
    def test_18_static_url(self):
        self.assertTrue(settings.is_overridden('STATIC_URL'))
        self.assertEquals(str, type(settings.STATIC_URL))
        self.assertEquals('/static/', settings.STATIC_URL) 
    
    def test_19_templates(self):
        templates = [{'APP_DIRS': True,
                      'BACKEND': 'django.template.backends.django.DjangoTemplates',
                      'DIRS': ['/Users/tim/Project/django-review/legacy/legacy/templates'],
                      'OPTIONS': {'context_processors': ['django.template.context_processors.debug',
                                                         'django.template.context_processors.request',
                                                         'django.contrib.auth.context_processors.auth',
                                                         'django.contrib.messages.context_processors.messages']}}]
        self.assertTrue(settings.is_overridden('TEMPLATES'))
        self.assertEquals(list, type(settings.TEMPLATES))
        self.assertListEqual(templates, settings.TEMPLATES) 
    
    def test_20_test_runner(self):
        self.assertTrue(settings.is_overridden('TEST_RUNNER'))
        self.assertEquals(str, type(settings.TEST_RUNNER))
        self.assertEquals('django_nose.NoseTestSuiteRunner', settings.TEST_RUNNER) 
    
    def test_21_time_zone(self):
        self.assertTrue(settings.is_overridden('TIME_ZONE'))
        self.assertEquals(str, type(settings.TIME_ZONE))
        self.assertEquals('UTC', settings.TIME_ZONE) 
    
    def test_22_use_i18n(self):
        self.assertTrue(settings.is_overridden('USE_I18N'))
        self.assertEquals(bool, type(settings.USE_I18N))
        self.assertTrue(settings.USE_I18N) 
    
    def test_23_use_l10n(self):
        self.assertTrue(settings.is_overridden('USE_L10N'))
        self.assertEquals(bool, type(settings.USE_L10N))
        self.assertTrue(settings.USE_L10N) 
    
    def test_24_use_tz(self):
        self.assertTrue(settings.is_overridden('USE_TZ'))
        self.assertEquals(bool, type(settings.USE_TZ))
        self.assertTrue(settings.USE_TZ) 
    
    def test_24_wsgi_application(self):
        self.assertTrue(settings.is_overridden('WSGI_APPLICATION'))
        self.assertEquals(str, type(settings.WSGI_APPLICATION))
        self.assertEquals('legacy.wsgi.application', settings.WSGI_APPLICATION) 
