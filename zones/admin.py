from django.contrib import admin

from dnsman.zones.models import Zone

class ZoneAdmin(admin.ModelAdmin):
    list_display = ('domain', 'formatted_last_modified')
    list_filter = ['domain']
    search_fields = ['domain', 'definition']

admin.site.register(Zone, ZoneAdmin)
