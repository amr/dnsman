from django import template
from django.utils._os import safe_join
from django.template.loader import get_template_from_string

def parking_page_to_template(parking_page):
    return get_template_from_string(parking_page.template)
