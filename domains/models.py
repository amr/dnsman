from django.db import models

class Domain(models.Model):
    name = models.CharField('Name', unique=True, max_length=253, help_text='The domain name, e.g. "example.com"')

    def __unicode__(self):
        return self.name

    def redirections_count(self):
        return self.redirections.count()
    redirections_count.short_description = 'Redirections #'

    def all_redirections(self):
        from dnsman.redirections.models import Redirection
        return Redirection.objects.filter(models.Q(from_domain=self) | models.Q(to_domain=self))
    all_redirections = property(all_redirections)

    def varnish_purge_hash_patterns(self):
        patterns = []
        for redirection in self.all_redirections:
            patterns += redirection.varnish_purge_hash_patterns()
        return tuple(patterns)
