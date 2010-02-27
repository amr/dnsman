from dnsman.redirections.models import Redirection
from dnsman.redirections.forms import RedirectionForm
from django.contrib import admin

class RedirectionAdmin(admin.ModelAdmin):
    form = RedirectionForm
    fieldsets = [
        (None, {'fields': ['from_domain', 'to_domain']}),
        ('Advanced options', {'fields': ['full_uri', 'code', 'weight', 'enabled'], 'classes': ['collapse']}),
    ]
    list_display = ('from_domain', 'to_domain', 'full_uri', 'code', 'weight', 'enabled')
    list_filter = ['code', 'full_uri', 'enabled']
    search_fields = ['to_domain__name', 'from_domain__name']
    ordering = ['-weight']

admin.site.register(Redirection, RedirectionAdmin)
