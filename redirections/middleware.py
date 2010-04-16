"""
Perform actual redirections based on given request and configured redirections
"""

import time
from django.utils.http import http_date
from django.conf import settings
from django.views.decorators.cache import patch_cache_control
from dnsman.redirections.models import Redirection

class RedirectionsMiddleware(object):
    def process_request(self, request):
        for redirection in Redirection.objects.filter(enabled=True).order_by('-weight'):
            if redirection.match_request(request):
                response = redirection.to_response(request)

                patch_cache_control(response, no_cache=True, max_age=0)

                # Expires in the past to force no caching with HTTP/1.0 caches which do
                # not recognize cache-control.
                response['Expires'] = http_date(time.time() - 86400)

                # If Varnish integration is active, we permit Varnish to cache our response
                # despite the expires and cache-control headers.
                if settings.VARNISH_INTEGRATION:
                    response['X-Varnish-Can-Cache'] = 1

                return response
