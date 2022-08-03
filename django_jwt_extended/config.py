import json
from datetime import timedelta
from django.utils import timezone
from django.apps import apps
from .exceptions import (
    ConfigIsNotDict,
    InvalidJsonFormat,
    InvalidJwtAlgorithm,
    InvalidLocation,
    InvalidExpires,
)

allowed_algorithm = ('HS256',)
allowed_location = ('headers', 'cookies',)

class ConfigParser:

    def __init__(self, config: dict):
        if not isinstance(config, dict):
            raise ConfigIsNotDict()
        self.access_token_cookie_name = self.validate_access_token_cookie_name(config)
        self.refresh_token_cookie_name = self.validate_refresh_token_cookie_name(config)
        self.jwt_algorithm = self.validate_jwt_algorithm(config)
        self.token_location = self.validate_token_location(config)
        self.access_token_expires = self.validate_access_token_expires(config)
        self.refresh_token_expires = self.validate_refresh_token_expires(config)
        self.errors = self.customize_error(config)

    @staticmethod
    def validate_access_token_cookie_name(config: dict):
        access_cookie_name = config.get('ACCESS_TOKEN_COOKIE_NAME', 'access_token')
        return access_cookie_name
    
    @staticmethod
    def validate_refresh_token_cookie_name(config: dict):
        refresh_cookie_name = config.get('REFRESH_TOKEN_COOKIE_NAME', 'refresh_token')
        return refresh_cookie_name

    @staticmethod
    def validate_jwt_algorithm(config: dict):
        jwt_algorithm = config.get('ALGORITHM', 'HS256')
        if jwt_algorithm not in allowed_algorithm:
            raise InvalidJwtAlgorithm(jwt_algorithm, allowed_algorithm)
        return jwt_algorithm

    @staticmethod
    def validate_token_location(config: dict):
        token_location = config.get('LOCATION', ['headers', 'cookies'])
        if not (
            isinstance(token_location, list)
            and not (set(token_location) - set(allowed_location))
        ):
            raise InvalidLocation(token_location, allowed_location)
        return token_location

    @staticmethod
    def validate_access_token_expires(config: dict):
        expires = config.get('ACCESS_TOKEN_EXPIRES', timedelta(days=2))
        if isinstance(expires, int) and expires > 0:
            expires = timedelta(seconds=expires)
        if not isinstance(expires, timedelta):
            raise InvalidExpires('ACCESS_TOKEN')
        return expires

    @staticmethod
    def validate_refresh_token_expires(config: dict):
        expires = config.get('REFRESH_TOKEN_EXPIRES', timedelta(days=30))
        if isinstance(expires, int) and expires > 0:
            expires = timedelta(seconds=expires)
        if not isinstance(expires, timedelta):
            raise InvalidExpires('REFRESH_TOKEN')
        return expires

    @staticmethod
    def customize_error(config: dict):

        def validate_json(data: dict):
            try:
                json.dumps(data)
            except ValueError:
                return False
            return True

        default_error = {
            'JWT_NOT_FOUND_MSG': {'msg': 'JWT token not found'},
            'DECODE_ERROR_MSG': {'msg': 'Signature verification failed.'},
            'EXPIRED_TOKEN_MSG': {'msg': 'JWT token has expired'},
            'INVALID_TOKEN_TYPE_MSG': {'msg': "Invalid JWT token type"},
            'INVALID_NBF_MSG': {'msg': "The token is not yet valid (nbf)"},
            'BEARER_ERROR_MSG': {
                'msg':(
                        f"Missing 'Bearer' type in "
                        f"'Authorization' header."
                        f" Expected 'Authorization: "
                        f"Bearer <JWT>'"
                    )
            },
        }

        customized_error = {}
        for error in default_error.keys():
            target = config.get(error, default_error[error])
            if not validate_json(target):
                raise InvalidJsonFormat()

            customized_error[error] = target

        return customized_error
