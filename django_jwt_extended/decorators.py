from functools import wraps
from django.http import JsonResponse
from django.conf import settings
from django.apps import apps
from .request import _find_request_object
from .tokens import _find_jwt_token, _parse_jwt_token, _validate_payload
from .exceptions import (
	RequestNotFound,
	InvalidOptionalType,
	InvalidRefreshType,
	JWTNotFound,
	InvalidBearerFormat,
	InvalidTokenType,
	TokenTypeNotFound,
)
import jwt
from jwt.exceptions import (
	InvalidSignatureError,
	ImmatureSignatureError,
	ExpiredSignatureError,
)


def jwt_required(optional=False, refresh=False):
	"""View decorator"""
	if not isinstance(optional, bool):
		raise InvalidOptionalType(str(type(optional)))
	if not isinstance(refresh, bool):
		raise InvalidRefreshType(str(type(refresh)))

	def wrapper(fn):
		@wraps(fn)
		def decorator(*args, **kwargs):
			""""do something"""
			request = _find_request_object(*args, **kwargs)

			# Django Request 객체를 찾을 수 없을 경우
			if request is None:
				raise RequestNotFound(fn.__name__)
			config = apps.get_app_config('django_jwt_extended')
			jwt_token, location = _find_jwt_token(request, refresh, config)

			# 토큰을 찾을 수 없을 경우
			if not optional and jwt_token is None:
				raise JWTNotFound()
			# 토큰을 찾을 수 없지만, optional인 경우
			elif optional and jwt_token is None:
				return fn(*args, **kwargs)

			# header 토큰에 한하여, Bearer 포맷이 아닐 경우
			jwt_token = _parse_jwt_token(jwt_token, location)
			if jwt_token is None:
				raise InvalidBearerFormat()

			payload = jwt.decode(
				jwt_token, settings.SECRET_KEY,
				config.jwt_algorithm,
			)

			# 토큰의 유효기간, 액세스/리프레시 검증
			valid = _validate_payload(payload, 'refresh' if refresh else 'access')
			if valid == 'type not found':
				raise TokenTypeNotFound()
			if valid == 'invalid type':
				raise InvalidTokenType()

			request.META['jwt_payload'] = payload
			return fn(*args, **kwargs)
		return decorator
	return wrapper
