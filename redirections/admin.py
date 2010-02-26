from dnsman.redirections.models import Redirection
from django.contrib import admin

class RedirectionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['to_domain', 'type', 'from_domain', 'pattern']}),
        ('Advanced options', {'fields': ['full_uri', 'code', 'weight'], 'classes': ['collapse']}),
    ]
    list_display = ('source', 'to_domain', 'full_uri', 'code', 'weight')
    list_filter = ['code', 'full_uri']
    search_fields = ['to_domain', 'from_domain', 'pattern']
    ordering = ['-weight']

admin.site.register(Redirection, RedirectionAdmin)
