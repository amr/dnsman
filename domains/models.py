from django.db import models
from dnsman.parking.models import ParkingPage

class Domain(models.Model):
    name = models.CharField('Name', unique=True, max_length=253, help_text='The domain name, e.g. "example.com"')
    parking_page = models.ForeignKey(ParkingPage, null=True, help_text='If no redirections are defined for this domain, this parking page will be used to welcome its visitors')

    def __unicode__(self):
        return self.name

    def match_request(self, request):
        uri = request.get_host() + request.get_full_path()
        
        import re
        pattern = "^(www\.)?%s" % re.escape(str(self))
        return re.compile(pattern, re.IGNORECASE).match(uri)

    def redirections_count(self):
        return self.redirections.count()
    redirections_count.short_description = 'Redirections #'

    def redirection_target(self):
        return self.redirects_to.to_domain
    redirection_target.short_description = 'Redirects to'

    def summary(self):
        from django.core.urlresolvers import reverse
        from django.utils.http import urlencode
        from django.utils.safestring import mark_safe
        from dnsman.redirections.models import Redirection
        
        try:
            return 'Redirects to: <a href="%s">%s</a>' % (
                reverse('admin:domains_domain_change', args=[self.redirects_to.to_domain.id]),
                self.redirects_to.to_domain,
            )
        except Redirection.DoesNotExist:
            pass
        
        summary = []
        if self.redirections.count():
            summary.append('Is redirected to from <a href="%s?%s">%d other domains</a>' % (
                reverse('admin:redirections_redirection_changelist'),
                urlencode({'q': self.name}),
                self.redirections.count(),
            ))
        if self.parking_page:
            summary.append('Displays parking page: <a href="%s">%s</a>' % (
                reverse('admin:parking_parkingpage_change', args=[self.parking_page.id]),
                mark_safe(self.parking_page),
            ))
        
        if len(summary):
            return ', '.join(summary)
        else:
            return None
    summary.short_description = 'Summary'
    summary.allow_tags = True

    def all_redirections(self):
        from dnsman.redirections.models import Redirection
        return Redirection.objects.filter(models.Q(from_domain=self) | models.Q(to_domain=self))
    all_redirections = property(all_redirections)

    def varnish_purge_hash_patterns(self):
        patterns = []
        for redirection in self.all_redirections:
            patterns += redirection.varnish_purge_hash_patterns()
        return tuple(patterns)
