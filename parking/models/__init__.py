from django.conf import settings
from django.db import models
from dnsman.parking.models.fields import DirectoryPathField

class ParkingPage(models.Model):
    name = models.CharField(max_length=32, help_text='Unique human-readable identifier for this parking page')
    template = models.TextField(help_text='Edit the parking page XHTML template')
    extends = models.ForeignKey('ParkingPage', null=True, blank=True, help_text='You may extend an existing parking page by selecting it. Read more about template inheritance: http://docs.djangoproject.com/en/1.1/topics/templates/#id1')
    resources_dir = DirectoryPathField(path=settings.PARKING_PAGES_DIR, blank=True, help_text='The directory which contains the external resources for the page, such as CSS and Images')
    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    def to_response(self, request):
        """Return an HttpResponse of this parking page for given request"""
        from dnsman.parking.template import parking_page_to_template
        t = parking_page_to_template(self)
        
        from django.http import HttpResponse
        from django.template import RequestContext
        response = HttpResponse(t.render(RequestContext(request)))
        
        return response
