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

    domain = models.ForeignKey(Domain, help_text='The destination domain')
    pattern = models.CharField(max_length=512, help_text='PCRE pattern to match the incoming request against')
    full_uri = models.BooleanField('Full URI?', default=True, help_text='Whether the redirect should include the full original URI (i.e. including the path and query string) or should forward to the root of the domain (i.e. /)')
    code = models.IntegerField(choices=REDIRECTION_CODES, default=301, help_text='The HTTP redirection code')
    label = models.CharField(max_length=32, blank=True, help_text='Human-readable label for this redirection rule, for use in the administration interface')

    def __unicode__(self):
        if len(self.label):
            return "%s => %s [%d]" % (self.label, self.domain, self.code)
        else:
            return "%s => %s [%d]" % (self.pattern, self.domain, self.code)
