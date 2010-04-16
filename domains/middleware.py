"""
Serves parking pages based on given request and configured domains parking pages
"""

import time
from django.conf import settings
from django.utils.http import http_date
from django.views.decorators.cache import patch_cache_control
from dnsman.redirections.models import Domain

class ParkingPagesMiddleware(object):
    def process_request(self, request):
        for domain in Domain.objects.exclude(parking_page=None):
            if domain.match_request(request) and domain.parking_page.match_request(request):
                response = domain.parking_page.to_response(request, domain)
                
                patch_cache_control(response, no_cache=True, max_age=0)
                
                # Expires in the past to force no caching with HTTP/1.0 caches which do
                # not recognize cache-control.
                response['Expires'] = http_date(time.time() - 86400)

                # If Varnish integration is active, we permit Varnish to cache our response
                # despite the expires and cache-control headers.
                if settings.VARNISH_INTEGRATION:
                    from dnsman.varnish_integration.cache import varnish_can_cache
                    varnish_can_cache(response)

                return response
