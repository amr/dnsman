from dnsman.redirections.models import Redirection
from django.contrib import admin

class RedirectionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['from_domain', 'to_domain']}),
        ('Advanced options', {'fields': ['full_uri', 'code', 'weight'], 'classes': ['collapse']}),
    ]
    list_display = ('from_domain', 'to_domain', 'full_uri', 'code', 'weight')
    list_filter = ['code', 'full_uri']
    search_fields = ['to_domain', 'from_domain']
    ordering = ['-weight']

admin.site.register(Redirection, RedirectionAdmin)
