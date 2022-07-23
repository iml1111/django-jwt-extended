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

        self.jwt_not_found_msg = data.jwt_not_found_msg
        self.bearer_error_msg = data.bearer_error_msg
        self.decode_error_msg = data.decode_error_msg
        self.expired_token_msg = data.expired_token_msg
        self.invalid_token_type_msg = data.invalid_token_type_msg
        self.invalid_nbf_msg = data.invalid_nbf_msg
        