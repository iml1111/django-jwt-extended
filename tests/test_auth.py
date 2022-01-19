import unittest, json, jwt
from django.conf import settings
from django.test import RequestFactory
from django.apps import apps
from tests.sample.views import (
    login, refresh, 
    user, user_optional,
    RestAPIView, rest_user
)


class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.access_token, self.refresh_token = self._get_tokens()
        self.methods = (
            self.factory.get,
            self.factory.post,
            self.factory.put,
            self.factory.delete,
        )

    def tearDown(self):
        pass

    def test_auth_basic(self):
        """Run Authentication basic"""
        request = self.factory.get(
            '/user',
            HTTP_Authorization=(
                "Bearer " + self.access_token
            )
        )
        response = user(request)
        self.assertEqual(response.status_code, 200)

    def test_refresh(self):
        """Run Token Refresh & reauth"""
        request = self.factory.get(
            '/refresh',
            HTTP_Authorization=(
                "Bearer "
                + self.refresh_token
            )
        )
        response = refresh(request)
        self.assertEqual(response.status_code, 200)
        tokens = json.loads(response.content)
        access_token = tokens['access_token']

        request = self.factory.get(
            '/user',
            HTTP_Authorization=(
                "Bearer "
                + access_token
            )
        )
        response = user(request)
        self.assertEqual(response.status_code, 200)

    def test_auth_optional(self):
        """Run Auth Optional"""
        auth_request = self.factory.get(
            '/user_optional',
            HTTP_Authorization=(
                "Bearer " + self.access_token
            )
        )
        no_auth_request = self.factory.get('/user_optional')

        response = user_optional(auth_request)
        self.assertEqual(response.status_code, 200)
        response = user_optional(no_auth_request)
        self.assertEqual(response.status_code, 200)

    def test_rest_api_class(self):
        """Run REST API View Class Auth"""
        view = RestAPIView.as_view()

        path = "/rest-api-class"
        token = "Bearer " + self.access_token
        for method in self.methods:
            request = method(path, HTTP_Authorization=token)
            response = view(request)
            self.assertEqual(response.status_code, 200)

    def test_rest_api_func(self):
        """Run REST API View Func Auth"""
        path = "/rest-api-func"
        token = "Bearer " + self.access_token
        for method in self.methods:
            request = method(path, HTTP_Authorization=token)
            response = rest_user(request, "hello")
            self.assertEqual(response.status_code, 200)

    def test_invalid_token_auth(self):
        """Run Invalid Token Auth"""
        payload = {'sub': 'invalid'}
        algorithm = 'HS256'
        secret_key = "invalid"
        invalid_token = jwt.encode(payload, secret_key, algorithm)

        request = self.factory.get(
            '/user',
            HTTP_Authorization=(
                "Bearer " + invalid_token
            )
        )
        response = user(request)
        self.assertEqual(response.status_code, 401)

    def test_token_not_found(self):
        """Test No Input Token Auth"""
        request = self.factory.get('/user')
        response = user(request)
        self.assertEqual(response.status_code, 401)

    def test_expired_token_auth(self):
        """Test Expired Token Auth"""
        payload = {'sub': 'iml', 'exp': 1}
        algorithm = 'HS256'
        secret_key = settings.SECRET_KEY
        exp_token = jwt.encode(payload, secret_key, algorithm)

        request = self.factory.get(
            '/user',
            HTTP_Authorization=(
                "Bearer " + exp_token
            )
        )
        response = user(request)
        self.assertEqual(response.status_code, 401)

    def _get_tokens(self):
        request = self.factory.get('/login')
        response = login(request)
        self.assertEqual(response.status_code, 200)

        tokens = json.loads(response.content)
        access_token = tokens['access_token']
        refresh_token = tokens['refresh_token']
        return access_token, refresh_token


if __name__ == '__main__':
    unittest.main()