from django.conf import settings
from django.db import models

import os.path

from dnsman.domains.models import Domain

class Zone(models.Model):
    domain = models.OneToOneField(Domain, related_name='zone', help_text='The delegated portion of the DNS namespace this zone assumes responsibility for')
    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.domain)

    def formatted_last_modified(self):
        return self.last_modified.strftime('%Y-%m-%d %H:%M:%S')
    formatted_last_modified.short_description = 'Last modified'
    formatted_last_modified.admin_order_field = 'last_modified'

    def get_definition(self):
        if os.path.exists(self.get_zone_file_path()):
            f = open(self.get_zone_file_path(), 'r')
            zone = f.read()
            f.close()
            return zone
        else:
            return ""

    def set_definition(self, definition):
        f = open(self.get_zone_file_path(), 'w')
        f.write(definition)
        f.close()

    def get_zone_file_path(self):
        return os.path.join(settings.ZONES_PATH, self.domain.name)

    definition = property(get_definition, set_definition)
