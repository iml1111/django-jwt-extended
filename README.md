# Django-JWT-Extended

![Python versions](https://img.shields.io/pypi/pyversions/django-jwt-extended) ![License](https://img.shields.io/badge/license-MIT-green) ![Release](https://img.shields.io/pypi/v/django-jwt-extended)

Implement JWT authentication with Django quickly and easily!
**Inspired by [flask-jwt-extended](https://github.com/vimalloc/flask-jwt-extended).**



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



# Advanced Usage

...



# Configuration

Even if you don't configure anything, your app works.

But in `settings.py` in your app, You can customize your app through the following settings.

## SECRET_KEY

This is the secret key setting that Django supports by default. 

`Django-jwt-extended` also, the key is used when encoding/decoding JWT.

## JWT_CONFIG

`JWT_CONFIG` is a setting added for `django_jwt_extended`. 

Additional settings can be added as follows in the form of a dictionary.

### ALGORITHM

`ALGORITHM: "HS256" `

- default: `HS256`
- allowed_values: `HS256`

Select the encode/decode algorithm for issuing tokens. (Currently only '**HS256**' is supported)

### LOCATION

`LOCATION: ["headers"]`

- default: `["headers"]`
- allowed_values: `headers`, `cookies`

This setting determines where to collect the Tokens. The thing to note is that **input is received as a list, not as a single string**. You can pass in a list to check more then one location, for example `["headers", "cookies"]`. The order of the list sets the precedence of where JWTs will be looked for.

### ACCESS_TOKEN_EXPIRES

`ACCESS_TOKEN_EXPIRES: 60 * 24 * 2 # 2days`

- default: `60 * 24 * 2`
- allowed_types: integer

How long an access token should be valid before it expires. This can be a a number of seconds (`Integer`).

### REFRESH_TOKEN_EXPIRES

`REFRESH_TOKEN_EXPIRES: 60 * 24 * 30 # 1month`

- default: `60 * 24 * 30`
- allowed_types: integer

How long a refresh token should be valid before it expires. This can be a number of seconds (`Integer`).

### Custom Error Responses

When your app encounters different situations, returns different error responses. When your app encounters different situations, it returns different error responses.

- JWT_NOT_FOUND_MSG

When your app encounters different situations, it returns different error responses.

- DECODE_ERROR_MSG

- EXPIRED_TOKEN_MSG

- INVALID_TOKEN_TYPE_MSG

- INVALID_NBF_MSG

- BEARER_ERROR_MSG

