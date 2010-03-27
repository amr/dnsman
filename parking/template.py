from django.template import TemplateDoesNotExist
from django.template.loader import BaseLoader, get_template_from_string
from dnsman.parking.models import ParkingPage

def parking_page_to_template(parking_page):
    template = parking_page.template
    if parking_page.extends:
        extends = '{%% extends "parking-page:%s" %%}' % parking_page.extends.id
        template = extends + '\n' + template
    return get_template_from_string(template)

class Loader(BaseLoader):
    """
    Wrapper for loading parking pages' templates. Allows using a special syntax
    for identifying the parking page: "parking-page:<id>"
    """

    is_usable = True

    def load_template_source(self, template_name, template_dirs=None):
        if template_name.startswith('parking-page:'):
            pid = template_name.split(':')[1]
            parking_page = ParkingPage.objects.get(pk=pid)
            if parking_page:
                return (unicode(parking_page.template), unicode(parking_page))
        raise TemplateDoesNotExist(template_name)
    load_template_source.is_usable = True
