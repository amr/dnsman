import time
from django.conf import settings
from django.utils.http import http_date
from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.cache import cache_control

from dnsman.redirections.models import Redirection
from dnsman.domains.models import Domain

@cache_control(no_cache=True, max_age=0)
def redirect(request):
    """Perform actual redirections based on given request and configured
    redirections"""

    response = None
    # TODO: This can be refactored to use a query for better performance
    for redirection in Redirection.objects.order_by('-weight'):
        if redirection.match_request(request):
            response = redirection.to_response(request)
            break

    if response is None:
        # TODO: This can be refactored to use a query for better performance
        for domain in Domain.objects.all():
            if domain.match_request(request):
                response = domain.parking_page.to_response(request)
                break

    if response is None:
        response = HttpResponseServerError('No redirection matched!')

    # Expires in the past to force no caching with HTTP/1.0 caches which do
    # not recognize cache-control.
    response['Expires'] = http_date(time.time() - 86400)

    # If Varnish integration is active, we permit Varnish to cache our response
    # despite the expires and cache-control headers.
    if settings.VARNISH_INTEGRATION:
        response['X-Varnish-Can-Cache'] = 1

    return response
