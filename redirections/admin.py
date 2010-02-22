from dnsman.redirections.models import Redirection
from django.contrib import admin

class RedirectionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['pattern', 'domain', 'full_uri', 'code']}),
        ('More options', {'fields': ['weight', 'label'], 'classes': ['collapse']}),
    ]
    list_display = ('pattern', 'domain', 'full_uri', 'code', 'weight')
    list_filter = ['code', 'full_uri']
    search_fields = ['domain', 'pattern']
    ordering = ['-weight']

admin.site.register(Redirection, RedirectionAdmin)
