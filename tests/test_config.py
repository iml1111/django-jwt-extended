import unittest
from datetime import timedelta
from django_jwt_extended.config import ConfigParser
from django_jwt_extended.exceptions import (
    InvalidJwtAlgorithm,
    InvalidLocation,
    InvalidExpires,
)
from django.apps import apps


class ConfigParserTestCase(unittest.TestCase):

    def setUp(self):
        self.config_parser = ConfigParser

    def tearDown(self):
        pass

    def test_valid_jwt_algorithm(self):
        """Validate JWT algorithm config"""
        self.config_parser.validate_jwt_algorithm({})
        self.config_parser.validate_jwt_algorithm(
            {'ALGORITHM': 'HS256'}
        )
        try:
            self.config_parser.validate_jwt_algorithm(
                {'ALGORITHM': 'BAD_ALGO'}
            )
            self.assertFalse(True)
        except InvalidJwtAlgorithm:
            pass
        
    def test_valid_token_location(self):
        """Validate JWT Token location config"""
        self.config_parser.validate_token_location({})
        self.config_parser.validate_token_location(
            {'LOCATION': ['headers']}
        )
        try:
            self.config_parser.validate_token_location(
                {'LOCATION': ['header']})
            self.config_parser.validate_token_location(
                {'LOCATION': 'header'})
            self.assertFalse(True)
        except InvalidLocation:
            pass
        
    def test_valid_token_expires(self):
        """Validate Token Expires config"""
        cases = [
            (
                self.config_parser.validate_access_token_expires, 
                'ACCESS_TOKEN_EXPIRES'
            ),
            (
                self.config_parser.validate_refresh_token_expires, 
                'REFRESH_TOKEN_EXPIRES'
            ),
        ]
        for module, key, in cases:
            module({})
            module({key: 100})
            module({key: timedelta(days=1)})
            try:
                module({key: -1})
                module({key: "INVALID"})
                self.assertFalse(True)
            except InvalidExpires:
                pass
        

if __name__ == '__main__':
    unittest.main()