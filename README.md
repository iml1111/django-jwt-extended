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

This section goes into more detail about django-jwt-extended.

## Return with refresh token

If you want to return not only the access token but also the refresh token, you can use it as follows.

```python
from django_jwt_extended import create_access_token
from django_jwt_extended import create_refresh_token

# Login and issue tokens
def login(request):
    return JsonResponse({
        "access_token": create_access_token("iml"),
        'refresh_token': create_refresh_token('iml'),
    })
```

## Refresh Token Authentication

## Optional Authentication

## Parse JWT Payload

## Custom Decorator





# Configuration

Even if you don't configure anything, your app works.

But in `settings.py` in your app, You can customize your app through the following settings. 

Here's a good sample.

```python
# settings.py

SECRET_KEY = "super-secret"

JWT_CONFIG = {
  'ALGORITHM': 'HS256',
  'LOCATION': ['headers'],
  'ACCESS_TOKEN_EXPIRES': timedelta(days=2),
  'REFRESH_TOKEN_EXPIRES': timedelta(days=30),
  'JWT_NOT_FOUND_MSG': {'msg': "can't find JWT token."}
}
...
```



## SECRET_KEY

This is the secret key setting that Django supports by default. 

`Django-jwt-extended` also, the key is used when encoding/decoding JWT.

## JWT_CONFIG

`JWT_CONFIG` is a setting added for `django_jwt_extended`. 

Additional settings can be added as follows in the form of a dictionary.

### ALGORITHM

`ALGORITHM: "HS256" `

- Default: `HS256`
- Allowed_values: `HS256`

Select the encode/decode algorithm for issuing tokens. (Currently only '**HS256**' is supported)

### LOCATION

`LOCATION: ["headers", ...]`

- default: `["headers"]`
- allowed_values: `headers`, `cookies`

This setting determines where to collect the Tokens. The thing to note is that **input is received as a list, not as a single string**. You can pass in a list to check more then one location, for example `["headers", "cookies"]`. The order of the list sets the precedence of where JWTs will be looked for.

- **headers**

For headers, the header name is fixed to **"Authorization"**, and the token format is **"Bearer [token]"**.

- **cookies**

 In the cookie, you can directly specify **the cookie name for the access token** and **the cookie name for the refresh token.**

### ACCESS_TOKEN_COOKIE_NAME

`ACCESS_TOKEN_COOKIE_NAME: access_token`

- Default: `access_token`
- Allowed_types: `string`

The name of the cookie that will hold the access token.

### REFRESH_TOKEN_COOKIE_NAME

`REFRESH_TOKEN_COOKIE_NAME: refresh_token`

- Default: `refresh_token`
- Allowed_types: `string`

The name of the cookie that will hold the refresh token.

### ACCESS_TOKEN_EXPIRES

`ACCESS_TOKEN_EXPIRES: 60 * 24 * 2 # 2days`

- Default: `60 * 24 * 2`
- Allowed_types: `integer`, `datetime.timedelta`

How long an access token should be valid before it expires. This can be a a number of seconds (`Integer`).

### REFRESH_TOKEN_EXPIRES

`REFRESH_TOKEN_EXPIRES: 60 * 24 * 30 # 1month`

- Default: `60 * 24 * 30`
- Allowed_types: `integer`, `datetime.timedelta`

How long a refresh token should be valid before it expires. This can be a number of seconds (`Integer`).

### Custom Error Responses

`<CUSTOM_ERROR_RESONSE>: {msg: "custom-error"}`

- Default: `[json-object]`
- Allowed_types: `Dict (json serializable)`

When your app encounters different situations, returns different error responses with 401. When your app encounters different situations, it returns different error responses.

- **JWT_NOT_FOUND_MSG**

When your app encounters different situations, it returns different error responses.

- **DECODE_ERROR_MSG**

Returned when the Token signature value is invalid.

- **EXPIRED_TOKEN_MSG**

If the corresponding token has expired, it will be returned.

- **INVALID_TOKEN_TYPE_MSG**

In case of an unexpected token type (access or refresh), it is returned.

- **INVALID_NBF_MSG**

If the nbf value does not exceed the current time, it is returned.

- **BEARER_ERROR_MSG**

Returned if token was found in Header, but does not start with Bearer.
