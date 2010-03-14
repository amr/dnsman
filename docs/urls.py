from django.conf.urls.defaults import *
from dnsman.docs.views import simple_doc

urlpatterns = patterns('',
    url('^(?P<uri>.+)?$',
        simple_doc,
        name='docs'
    ),
)
