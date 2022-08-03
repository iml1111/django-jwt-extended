from datetime import datetime
from uuid import uuid4
import jwt
from django.apps import apps
from django.http import HttpRequest
from django.conf import settings
from .apps import DjangoJwtExtConfig
from .request import REQUESTS
from .exceptions import InvalidRequest


def create_access_token(identity):
    config = apps.get_app_config('django_jwt_extended')
    payload = _create_payload(identity, 'access', config)
    return jwt.encode(
        payload=payload,
        key=settings.SECRET_KEY,
        algorithm=config.jwt_algorithm
    )


def create_refresh_token(identity):
    config = apps.get_app_config('django_jwt_extended')
    payload = _create_payload(identity, 'refresh', config)
    return jwt.encode(
        payload=payload,
        key=settings.SECRET_KEY,
        algorithm=config.jwt_algorithm
    )


def get_jwt_identity(request: HttpRequest):
    if not any([isinstance(request, obj) for obj in REQUESTS]):
        raise InvalidRequest(str(type(request)))
    if 'jwt_payload' in request.META:
        return request.META['jwt_payload'].get('sub')
    else:
        return None


def get_jwt(request: HttpRequest):
    if not any([isinstance(request, obj) for obj in REQUESTS]):
        raise InvalidRequest(str(type(request)))
    return request.META.get('jwt_payload')


"""Inner Func"""
def _create_payload(identity, type: str, config: DjangoJwtExtConfig):
    if type == 'access':
        expires = config.access_token_expires
    else:
        expires = config.refresh_token_expires
    now = datetime.utcnow()
    return {
        'iat': now,
        'jti': str(uuid4()),
        'type': type,
        'sub': identity,
        'nbf': now,
        'exp': now + expires,
    }


def _find_jwt_token(request, refresh: bool, config: DjangoJwtExtConfig):
    for location in config.token_location:
        if (
            location == 'headers'
            and config.token_header_name in request.headers
        ):
            return request.headers[config.token_header_name], location

        elif location == 'cookies':
            if not refresh and config.access_token_cookie_name in request.COOKIES:
                return request.COOKIES[config.access_token_cookie_name], location
            elif refresh and config.refresh_token_cookie_name in request.COOKIES:
                return request.COOKIES[config.refresh_token_cookie_name], location

    return None, None


def _parse_jwt_token(jwt_token: str, location: str):
    if location == 'headers':
        if jwt_token.startswith('Bearer '):
            return jwt_token[7:]
    elif location == 'cookies':
        return jwt_token
    else:
        return None


def _validate_payload(payload: dict, type: str):
    if payload['type'] != type:
        return 'invalid type'
    else:
        return "valid"