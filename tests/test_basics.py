import unittest
from django.apps import apps

class BasicsTestCase(unittest.TestCase):

    def setUp(self):
        self.config = apps.get_app_config('django_jwt_extended')

    def tearDown(self):
        pass

    def test_module_exists(self):
        """Run Module Exists"""
        self.assertFalse(self.config is None)

    def test_config_exists(self):
        """App config Exists"""
        keys = (
            'jwt_algorithm',
            'token_location',
            'access_token_expires',
            'refresh_token_expires',
            'token_header_name',
        )
        for key in keys:
            self.assertTrue(hasattr(self.config, key))

if __name__ == '__main__':
    unittest.main()