from django.conf import settings
from django.db import models, transaction
from django.template.defaultfilters import slugify

from dnsman.parking.models.fields import DirectoryPathField
from dnsman.parking import PARKING_PAGES_ROOT, PARKING_PAGES_URL

class ParkingPage(models.Model):
    name = models.CharField(max_length=32, unique=True, help_text='Unique human-readable identifier for this parking page, example: "N2V Standard"')
    template = models.TextField(null=True, blank=True, help_text='Edit the parking page HTML template right in the browser')
    extends = models.ForeignKey('ParkingPage', null=True, blank=True, help_text='You may extend an existing parking page by selecting it. Read more about template inheritance: http://docs.djangoproject.com/en/1.1/topics/templates/#id1')
    resources_dir = DirectoryPathField(path=PARKING_PAGES_ROOT, default="[auto]", help_text="The directory which contains the external resources for the page, such as CSS and Images. Choose [auto-create] and a directory will be automatically created. To add a directory manually, you need to place it under %s" % PARKING_PAGES_ROOT)
    last_modified = models.DateTimeField(auto_now=True)

    @transaction.commit_on_success
    def delete(self, keep_resources=False, using=None):
        super(ParkingPage, self).delete(using)

        if not keep_resources:
            import shutil
            shutil.rmtree(self.resources_dir_fullpath)

    def __unicode__(self):
        return self.name

    def resources_dir_fullpath(self):
        import os.path
        return os.path.join(PARKING_PAGES_ROOT, self.resources_dir)
    resources_dir_fullpath = property(resources_dir_fullpath)

    def formatted_last_modified(self):
        return self.last_modified.strftime('%Y-%m-%d %H:%M:%S')
    formatted_last_modified.short_description = 'Last modified'
    formatted_last_modified.admin_order_field = 'last_modified'

    def used_in(self):
        if self.domain_set.count():
            from django.core.urlresolvers import reverse
            from django.utils.http import urlencode
            return '<a href="%s?%s">%d domains</a>' % (
                reverse('admin:domains_domain_changelist'),
                urlencode({'q': self.name}),
                self.domain_set.count(),
            )
    used_in.allow_tags = True

    def render(self, request, domain, extra_context=None):
        """Render based on given request and domain"""
        from dnsman.parking.template import parking_page_to_template
        t = parking_page_to_template(self)

        if PARKING_PAGES_URL.startswith('http'):
            absolute_base_path = "%s/%s/" % (
                PARKING_PAGES_URL.rstrip('/'),
                self.resources_dir.rstrip('/'),
            )
        else:
            absolute_base_path = "%s://%s/%s/%s/" % (
                request.is_secure() and 'https' or 'http',
                request.get_host().rstrip('/'),
                PARKING_PAGES_URL,
                self.resources_dir.rstrip('/'),
            )

        from django.template import Context
        c = Context({
            'absolute_base_path': absolute_base_path,
            'domain': unicode(domain.name),
        })
        c.update(extra_context or {})
        return t.render(c)

    def to_response(self, request, domain):
        """Return an HttpResponse of this parking page for given request"""
        from django.http import HttpResponse
        return HttpResponse(self.render(request, domain))

    def auto_dir(self, field):
        return slugify(self.name)

