from django.conf import settings
from django.db import models, transaction
from django.template.defaultfilters import slugify

from dnsman.parking.models.fields import DirectoryPathField

class ParkingPage(models.Model):
    name = models.CharField(max_length=32, unique=True, help_text='Unique human-readable identifier for this parking page, example: "N2V Standard"')
    template = models.TextField(null=True, blank=True, help_text='Edit the parking page HTML template right in the browser')
    extends = models.ForeignKey('ParkingPage', null=True, blank=True, help_text='You may extend an existing parking page by selecting it. Read more about template inheritance: http://docs.djangoproject.com/en/1.1/topics/templates/#id1')
    resources_dir = DirectoryPathField(path=settings.PARKING_PAGES_DIR, default="[auto]", help_text="The directory which contains the external resources for the page, such as CSS and Images. Choose [auto-create] and a directory will be automatically created. To add a directory manually, you need to place it under %s" % settings.PARKING_PAGES_DIR)
    last_modified = models.DateTimeField(auto_now=True)

    @transaction.commit_on_success
    def delete(self, keep_resources=False, using=None):
        super(ParkingPage, self).delete(using)

        if not keep_resources:
            import shutil
            shutil.rmtree(self.resources_dir)

    def __unicode__(self):
        return self.name

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

    def to_response(self, request):
        """Return an HttpResponse of this parking page for given request"""
        from dnsman.parking.template import parking_page_to_template
        t = parking_page_to_template(self)
        
        from django.http import HttpResponse
        from django.template import RequestContext
        response = HttpResponse(t.render(RequestContext(request)))
        
        return response

    def auto_dir(self, field):
        return slugify(self.name)

