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
    enabled = models.BooleanField('Enabled?', db_index=True, default=True, help_text='Disable this redirect temporarily by checking off this option')
    last_modified = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.from_domain.parking_page:
            from django.core.exceptions import ValidationError
            raise ValidationError("Can't redirect from domain %s as it has an associated parking page" % self.from_domain)

    def match_request(self, request):
        return self.from_domain.match_request(request)

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

        # Last-modified
        import time
        from django.utils.http import http_date
        response['Last-Modified'] = http_date(time.mktime(self.last_modified.timetuple()))

        return response

    def varnish_purge_hash_patterns(self):
        # This requires that cache items hashing is left to the default, which
        # is "url+host"
        return (r".*%s" % self.from_domain,)

    def __unicode__(self):
            return "%s => %s [%d]" % (self.from_domain, self.to_domain, self.code)

    def formatted_last_modified(self):
        return self.last_modified.strftime('%Y-%m-%d %H:%M:%S')
    formatted_last_modified.short_description = 'Last modified'
    formatted_last_modified.admin_order_field = 'last_modified'

# Update last-modified of all related redirections when a domain changes.
def domain_saved(sender, created=None, instance=None, **kwargs):
    # We are only interested in updates
    if not created and instance is not None:
        import datetime
        instance.all_redirections.update(last_modified=datetime.datetime.now())
models.signals.post_save.connect(domain_saved, sender=Domain)
