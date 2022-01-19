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

        # default error messages
        self.jwt_not_found_msg = {
            'msg': 'JWT token not found'
        }
        self.bearer_error_msg = {
            'msg': (
                f"Missing 'Bearer' type in "
                f"'{self.token_header_name}' header."
				f" Expected '{self.token_header_name}: "
                f"Bearer <JWT>'"
            )
        }
        self.decode_error_msg = {
            'msg': 'Signature verification failed.'
        }
        self.expired_token_msg = {
            'msg': 'JWT Token has expired'
        }
        self.invalid_token_type_msg = {
            'msg': "Invalid JWT token type"
        }