import django
from .decorators import jwt_required
from .tokens import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
)

__AUTHOR__ = "IML"
__VERSION__ = "1.0.0"

default_app_config = 'django_jwt_extended.apps.DjangoJwtExtConfig'


