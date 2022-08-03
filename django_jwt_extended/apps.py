from datetime import timedelta
from django.apps import AppConfig
from django.conf import settings
from .config import ConfigParser
from .exceptions import NotFoundSecretKey


class DjangoJwtExtConfig(AppConfig):
    name = 'django_jwt_extended'
    verbose_name = "Django JWT Extended"

    def ready(self):
        if not hasattr(settings, 'SECRET_KEY'):
            raise NotFoundSecretKey()

        data = ConfigParser(
            settings.JWT_CONFIG
            if hasattr(settings, 'JWT_CONFIG')
            else {}
        )
        self.jwt_algorithm = data.jwt_algorithm
        self.token_location = data.token_location
        self.access_token_expires = data.access_token_expires
        self.refresh_token_expires = data.refresh_token_expires
        self.token_header_name = 'Authorization'
        self.access_token_cookie_name = data.access_token_cookie_name
        self.refresh_token_cookie_name = data.refresh_token_cookie_name

        self.jwt_not_found_msg = data.errors['JWT_NOT_FOUND_MSG']
        self.bearer_error_msg = data.errors['BEARER_ERROR_MSG']
        self.decode_error_msg = data.errors['DECODE_ERROR_MSG']
        self.expired_token_msg = data.errors['EXPIRED_TOKEN_MSG']
        self.invalid_token_type_msg = data.errors['INVALID_TOKEN_TYPE_MSG']
        self.invalid_nbf_msg = data.errors['INVALID_NBF_MSG']
        