from django.core.urlresolvers import resolve
from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from django.http import Http404


class SSLifyMiddleware(object):
    """Force all requests to use HTTPs. If we get an HTTP request, we'll just
    force a redirect to HTTPs.

    .. note::
        This will only take effect if ``settings.DEBUG`` is False.

    .. note::
        Stolen from: django-sslify
        and modified to only redirect urls in settings.URLS_TO_SSLIFY
        and redirect back to SITE_BASE_URL any urls which are not
    """

    def process_request(self, request):
        if not settings.DEBUG:
            # This will always build an http version of the url
            url = request.build_absolute_uri(request.get_full_path())
            # Therefore check if it's already secure
            X_FORWARDED_PROTO = request.META.get('HTTP_X_FORWARDED_PROTO', '')
            forwarded_https = X_FORWARDED_PROTO == 'https'
            already_secure = forwarded_https or request.is_secure()
            try:
                # Try to resolve the request path to a named url
                match = resolve(request.path)
                # See if that's one of the named urls we want to ssl-ify and is http
                if match.url_name in settings.URLS_TO_SSLIFY and not already_secure:
                    # Forcefully direct pages which should be https to HTTPS_URL
                    secure_url = url.replace(settings.SITE_BASE_URL, settings.HTTPS_URL)
                    return HttpResponsePermanentRedirect(secure_url)
                # See if it's not one of the ones we want to sslify, but is https
                elif match.url_name not in settings.URLS_TO_SSLIFY and already_secure:
                    # Forcefully redirect other https pages to SITE_BASE_URL
                    non_secure_url = url.replace(settings.HTTPS_URL, settings.SITE_BASE_URL)
                    return HttpResponsePermanentRedirect(non_secure_url)
            except Http404:
                # Doesn't match a url django knows
                pass
