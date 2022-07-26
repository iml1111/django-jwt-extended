# Django-JWT-Extended

![Python versions](https://img.shields.io/pypi/pyversions/django-jwt-extended) ![License](https://img.shields.io/badge/license-MIT-green) ![Release](https://img.shields.io/badge/release-1.0.0-red)

Implement JWT authentication with Django quickly and easily!



# Installation

**Pip**: `pip install django-jwt-extended`

After that, add `django_jwt_extended` to `INSTALLED_APPS` settings.

```
INSTALLED_APPS = [
    ...
    'django_jwt_extended',
]
```



# Get Started

`django-jwt-extended` makes it easy and simple to create authentication feature.

## Startup your project

```shell
$ pip install django
$ pip install django-jwt-extended
$ django-admin startproject example .
$ python manage.py migrate
$ python manage.py createsuperuser
```

## Edit your views

```python
# views.py
from django.http import JsonResponse
from django_jwt_extended import jwt_required
from django_jwt_extended import create_access_token
from django_jwt_extended import get_jwt_identity

def login(request):
    """Create JWT Token API"""
    return JsonResponse({
        "access_token": create_access_token(identity="iml"),
    })

@jwt_required()
def user(request):
    """JWT Authentication API"""
    identity = get_jwt_identity(request) # "iml"
    return JsonResponse({'id': identity,})
```



# Configuration

Even if you don't configure anything, this app works.

But In `settings.py` in your app, You can customize this app through the following settings.

## SECRET KEY

This is the secret key setting that Django supports by default. 

`Django-jwt-extended` also, the key is used when encoding/decoding JWT.



# Advanced Usage



