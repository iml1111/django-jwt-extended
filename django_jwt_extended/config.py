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
