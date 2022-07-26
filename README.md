# Django-JWT-Extended

![Python versions](https://img.shields.io/pypi/pyversions/django-jwt-extended) ![License](https://img.shields.io/badge/license-MIT-green) ![Release](https://img.shields.io/badge/release-1.0.0-red)

Implement JWT authentication with Django quickly and easily!



## Installation

**Pip**: `pip install django-jwt-extended`

그 후, `INSTALLED_APPS` settings에 `django_jwt_extended`를 추가해주세요.

```
INSTALLED_APPS = [
    ...
    'django_jwt_extended',
]
```



## Get Started

django-jwt-extended는 최대한 쉽고 간단하게 인증 기능을 구현할 수 있도록 만들었어요!

### Startup your project

```shell
$ pip install django
$ pip install django-jwt-extended
$ django-admin startproject example .
$ python manage.py migrate
$ python manage.py createsuperuser
```

### Edit your views

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



### **문서화 진행 중 입니다...😢**

