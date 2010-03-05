"""
Watches models defined in VARNISH_WATCHED_MODELS setting, and purges their
associated Varnish caches when they are updated.
"""

from django.conf import settings

def varnish_url_purge_handler(sender, created=None, instance=None, **kwargs):
    from varnishapp.manager import manager
    if not created and instance is not None:
        for pattern in instance.varnish_purge_hash_patterns():
            manager.run('purge.hash', pattern)

class VarnishIntegrationMiddleware(object):
    def process_request(self, request):
        if settings.VARNISH_INTEGRATION:
            from django.db.models.signals import post_save
            from django.db.models import get_model
            
            for model in getattr(settings, 'VARNISH_WATCHED_MODELS', ()):
                post_save.connect(varnish_url_purge_handler, sender=get_model(*model.split('.')))
