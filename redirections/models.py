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

    to_domain = models.ForeignKey(Domain, related_name='redirections', help_text='The domain to redirect to')
    full_uri = models.BooleanField('Full URI?', default=True, help_text='Whether the redirect should include the full original URI (i.e. including the path and query string) or should forward to the root of the domain (i.e. /)')
    code = models.IntegerField('HTTP Status Code', choices=REDIRECTION_CODES, default=301, help_text='The HTTP status code to use for the redirection')
    weight = models.SmallIntegerField(default=0, help_text='Governs the order of the evaluation of the redirection rules', choices=WEIGHTS)
    label = models.CharField(max_length=32, blank=True, help_text='Human-readable label for this redirection rule, for use in the administration interface')

    def match_request(self, request):
        """Check if given request matches this redirection"""
        raise NotImplementedError

    def to_response(self, request):
        """Return an HttpResponse of this redirection for given request"""
        from django.http import HttpResponse
        response = HttpResponse()
        response.status_code = self.code
        
        # "http://" must be configurable
        location = 'http://' + str(self.to_domain)
        if self.full_uri:
            location += request.get_full_path()
        else:
            location += '/'

        response['Location'] = location
        
        return response

class SimpleRedirection(Redirection):
    from_domain = models.OneToOneField(Domain, related_name='redirects_to', help_text='The domain to redirect from')

    def __unicode__(self):
        if len(self.label):
            return "%s => %s [%d]" % (self.label, self.to_domain, self.code)
        else:
            return "%s => %s [%d]" % (self.from_domain, self.to_domain, self.code)

    def match_request(self, request):
        uri = request.get_host() + request.get_full_path()
        
        import re
        pattern = "^(www\.)?%s" % re.escape(self.from_domain)
        return re.compile(pattern, re.IGNORECASE).match(uri)

class RegexRedirection(Redirection):
    pattern = models.CharField(max_length=512, help_text='PCRE pattern to match the incoming request against. Matching is case-insensitive')

    def __unicode__(self):
        if len(self.label):
            return "%s => %s [%d]" % (self.label, self.to_domain, self.code)
        else:
            return "%s => %s [%d]" % (self.pattern, self.to_domain, self.code)

    def match_request(self, request):
        uri = request.get_host() + request.get_full_path()

        import re
        return re.compile(self.pattern, re.IGNORECASE).match(uri)
