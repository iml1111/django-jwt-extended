from .exceptions import NotFoundRequest
from django.http import HttpRequest
from django.core.handlers.asgi import ASGIRequest
from django.core.handlers.wsgi import WSGIRequest
try:
    # If use django_rest_framework,
    from rest_framework.request import Request as RestRequest
    REQUESTS = (HttpRequest, ASGIRequest, WSGIRequest, RestRequest)
except:
    REQUESTS = (HttpRequest, ASGIRequest, WSGIRequest)


def _find_request_object(*args, **kwargs):
    for object in args:
        if any([isinstance(object, req) for req in REQUESTS]):
            return object
    for object in kwargs.values():
        if any([isinstance(object, req) for req in REQUESTS]):
            return object
    return None