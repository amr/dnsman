from django.conf import settings
import os.path

# Convenient variables which are frequently used
PARKING_PAGES_ROOT = os.path.join(settings.MEDIA_ROOT, settings.PARKING_PAGES_DIR)

PARKING_PAGES_URL = "%s/%s/" % (
    settings.MEDIA_URL.rstrip('/'),
    settings.PARKING_PAGES_DIR.strip('/'),
)
