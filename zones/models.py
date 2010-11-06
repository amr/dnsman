from django.db import models

from dnsman.domains.models import Domain

class Zone(models.Model):
    domain = models.OneToOneField(Domain, related_name='zone', help_text='The delegated portion of the DNS namespace this zone assumes responsibility for')
    definition = models.TextField(null=True, blank=True, help_text='The zone definition (the contents of the zone file)')
    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.domain)

    def formatted_last_modified(self):
        return self.last_modified.strftime('%Y-%m-%d %H:%M:%S')
    formatted_last_modified.short_description = 'Last modified'
    formatted_last_modified.admin_order_field = 'last_modified'
