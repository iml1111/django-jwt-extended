from datetime import timedelta
from django.utils import timezone
from django.apps import apps
from .exceptions import (
    ConfigIsNotDict,
    InvalidJwtAlgorithm,
    InvalidLocation,
    InvalidExpires,
)

allowed_algorithm = ('HS256',)
allowed_location = ('headers',)

class ConfigParser:

    def __init__(self, config: dict):
        if not isinstance(config, dict):
            raise ConfigIsNotDict()
        self.jwt_algorithm = self.validate_jwt_algorithm(config)
        self.token_location = self.validate_token_location(config)
        self.access_token_expires = self.validate_access_token_expires(config)
        self.refresh_token_expires = self.validate_refresh_token_expires(config)
        self.jwt_not_found_msg = self.customize_jwt_not_found(config)
        self.bearer_error_msg = self.customize_bearer_error(config)
        self.decode_error_msg = self.customize_decode_error(config)
        self.expired_token_msg = self.customize_expired_token(config)
        self.invalid_token_type_msg = self.customize_invalid_token_type(config)
        self.invalid_nbf_msg = self.customize_invalid_nbf(config)

    @staticmethod
    def validate_jwt_algorithm(config: dict):
        jwt_algorithm = config.get('ALGORITHM', 'HS256')
        if jwt_algorithm not in allowed_algorithm:
            raise InvalidJwtAlgorithm(jwt_algorithm, allowed_algorithm)
        return jwt_algorithm

    @staticmethod
    def validate_token_location(config: dict):
        token_location = config.get('LOCATION', ['headers'])
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
    def customize_jwt_not_found(config: dict):
        jwt_not_found = config.get('JWT_NOT_FOUND_MSG', 'JWT token not found')
        return {'msg': jwt_not_found}

    @staticmethod
    def customize_bearer_error(config: dict):
        bearer_error = config.get('BEARER_ERROR_MSG',
            (
                f"Missing 'Bearer' type in "
                f"'Authorization' header."
                f" Expected 'Authorization: "
                f"Bearer <JWT>'"
            )
        )
        return {'msg': bearer_error}

    @staticmethod
    def customize_decode_error(config: dict):
        decode_error = config.get(
            'DECODE_ERROR_MSG', 
            'Signature verification failed.'
        )
        return {'msg': decode_error}

    @staticmethod
    def customize_expired_token(config: dict):
        expired_token = config.get('EXPIRED_TOKEN_MSG', 'JWT Token has expired')
        return {'msg': expired_token}

    @staticmethod
    def customize_invalid_token_type(config: dict):
        invalid_token_type = config.get(
            'INVALID_TOKEN_TYPE_MSG', 
            "Invalid JWT token type"
        )
        return {'msg': invalid_token_type}
    
    @staticmethod
    def customize_invalid_nbf(config: dict):
        invalid_nbf = config.get(
            'INVALID_NBF_MSG', 
            "The token is not yet valid (nbf)"
        )
        return {'msg': invalid_nbf}

    
