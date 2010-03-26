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
    (r'^dnsman-admin/doc/', include('dnsman.docs.urls')),
    (r'^dnsman-admin/', include(admin.site.urls)),
    (r'^%s/(?P<path>.*)$' % settings.MEDIA_URL.strip('/'), 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}, 'media'),
    (r'', 'dnsman.redirections.views.redirect'),
)
