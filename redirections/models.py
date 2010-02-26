from django.utils.translation import ugettext as _

from django.db import models
from dnsman.domains.models import Domain

class Redirection(models.Model):
    REDIRECTION_CODES = (
        (301, '301 Moved Permanently'),
        (302, '302 Found'),
        (303, '303 See Other'),
        (304, '304 Not Modified'),
        (305, '305 Use Proxy'),
        (307, '307 Temporary Redirect')
    )

    WEIGHTS = zip(range(-10, 10), range(-10, 10))

    from_domain = models.OneToOneField(Domain, related_name='redirects_to', help_text='The domain to redirect from')
    to_domain = models.ForeignKey(Domain, related_name='redirections', help_text='The domain to redirect to')
    full_uri = models.BooleanField('Full URI?', default=True, help_text='Whether the redirect should include the full original URI (i.e. including the path and query string) or should forward to the root of the domain (i.e. /)')
    code = models.IntegerField('HTTP Status Code', choices=REDIRECTION_CODES, default=301, help_text='The HTTP status code to use for the redirection')
    weight = models.SmallIntegerField(default=0, help_text='Governs the order of the evaluation of the redirection rules', choices=WEIGHTS)

    def match_request(self, request):
        uri = request.get_host() + request.get_full_path()
        
        import re
        pattern = "^(www\.)?%s" % re.escape(self.from_domain)
        return re.compile(pattern, re.IGNORECASE).match(uri)

    def to_response(self, request):
        """Return an HttpResponse of this redirection for given request"""
        from django.http import HttpResponse
        response = HttpResponse()
        response.status_code = self.code
        
        location = 'http://' + str(self.to_domain)
        if self.full_uri:
            location += request.get_full_path()
        else:
            location += '/'

        response['Location'] = location
        
        return response

    def __unicode__(self):
            return "%s => %s [%d]" % (self.from_domain, self.to_domain, self.code)
