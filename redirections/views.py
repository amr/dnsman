from django.http import HttpResponse
from dnsman.redirections.models import Redirection

def redirect(request):
    """Perform actual redirections based on given request and configured
    redirections"""

    for redirection in Redirection.objects.order_by('-weight'):
        if redirection.match_request(request):
            return redirection.to_response(request)

    return HttpResponse("No redirection matched!")
