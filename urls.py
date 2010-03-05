from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = []

# Varnish Management, needs to come first
if settings.VARNISH_INTEGRATION:
    urlpatterns += patterns('',
        (r'^dnsman-admin/varnish/', include('varnishapp.urls'))
    )

urlpatterns += patterns('',
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^dnsman-admin/', include(admin.site.urls)),
    (r'', 'dnsman.redirections.views.redirect'),
)
