from django.core.urlresolvers import reverse
from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from django.test.client import RequestFactory
from django.http import HttpResponsePermanentRedirect

from ..middleware import SSLifyMiddleware as _SSLifyMiddleware


@override_settings(URLS_TO_SSLIFY=['home'],
                   SITE_BASE_URL='http://testserver',
                   HTTPS_URL='https://testserver')
class SSLifyMiddlewareTests(TestCase):

    def test_redirects_sslify_urls_to_https(self):
        factory = RequestFactory()
        request = factory.get(reverse('home'))
        absolute_uri = request.build_absolute_uri()
        self.assertTrue(absolute_uri.startswith(settings.SITE_BASE_URL))

        middleware = _SSLifyMiddleware()
        request = middleware.process_request(request)

        self.assertIsInstance(request, HttpResponsePermanentRedirect)
        self.assertTrue(request['Location'].startswith(settings.HTTPS_URL))

    def test_doesnt_redirect_already_https_sslify_urls(self):
        # Need to tell the RequestFactory to make https urls
        https_factory = RequestFactory(**{'wsgi.url_scheme': 'https'})
        request = https_factory.get(reverse('home'))
        absolute_uri = request.build_absolute_uri()
        self.assertTrue(absolute_uri.startswith(settings.HTTPS_URL))

        middleware = _SSLifyMiddleware()
        request = middleware.process_request(request)

        # We should ignore this url and do nothing with it
        self.assertIsNone(request)

    def test_doesnt_redirect_non_sslify_urls(self):
        # Need to tell the RequestFactory to make https urls
        factory = RequestFactory()
        request = factory.get(reverse('area'))
        absolute_uri = request.build_absolute_uri()
        self.assertTrue(absolute_uri.startswith(settings.SITE_BASE_URL))

        middleware = _SSLifyMiddleware()
        request = middleware.process_request(request)

        # We should ignore this url and do nothing with it
        self.assertIsNone(request)

    def test_redirects_https_non_sslify_urls_to_http(self):
        # Need to tell the RequestFactory to make https urls
        https_factory = RequestFactory(**{'wsgi.url_scheme': 'https'})
        request = https_factory.get(reverse('area'))
        absolute_uri = request.build_absolute_uri()
        self.assertTrue(absolute_uri.startswith(settings.HTTPS_URL))

        middleware = _SSLifyMiddleware()
        request = middleware.process_request(request)

        self.assertIsInstance(request, HttpResponsePermanentRedirect)
        self.assertTrue(request['Location'].startswith(settings.SITE_BASE_URL))
