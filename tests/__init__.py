from datetime import timedelta
import os, sys
import django



def setup_django():
    from django.conf import settings

    # USE_L10N is deprecated, and will be removed in Django 5.0.
    use_l10n = {"USE_L10N": True} if django.VERSION < (4, 0) else {}

    settings.configure(
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
            },
        },
        SECRET_KEY='not very secret in tests',
        USE_I18N = True,
        ROOT_URLCONF='tests.urls',
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'APP_DIRS': True,
                'OPTIONS': {
                    "debug": True,  # We want template errors to raise
                }
            },
        ],
        MIDDLEWARE=(
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ),
        INSTALLED_APPS=(
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.staticfiles',
            'rest_framework',
            'tests',
            'tests.sample',
            'django_jwt_extended',   
        ),
        JWT_CONFIG = {
            'ALGORITHM': 'HS256',
            'LOCATION': ['headers', 'cookies'],
            'ACCESS_TOKEN_EXPIRES': timedelta(days=2),
            'REFRESH_TOKEN_EXPIRES': timedelta(days=30),
            'JWT_NOT_FOUND_MSG': {'msg': "can't find JWT token."},
            'ACCESS_TOKEN_COOKIE_NAME': 'access_token',
            'REFRESH_TOKEN_COOKIE_NAME': 'refresh_token'
        },
        TIME_ZONE='Asia/Seoul',
        USE_TZ=False,
        **use_l10n,
    )

    django.setup()

setup_django()