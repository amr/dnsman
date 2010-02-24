from dnsman.redirections.models import SimpleRedirection, RegexRedirection
from django.contrib import admin

class SimpleRedirectionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['from_domain', 'to_domain']}),
        ('Advanced options', {'fields': ['full_uri', 'code', 'weight', 'label'], 'classes': ['collapse']}),
    ]
    list_display = ('from_domain', 'to_domain', 'full_uri', 'code', 'weight')
    list_filter = ['code', 'full_uri']
    search_fields = ['to_domain', 'from_domain']
    ordering = ['-weight']

class RegexRedirectionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['pattern', 'to_domain']}),
        ('Advanced options', {'fields': ['full_uri', 'code', 'weight', 'label'], 'classes': ['collapse']}),
    ]
    list_display = ('pattern', 'to_domain', 'full_uri', 'code', 'weight')
    list_filter = ['code', 'full_uri']
    search_fields = ['to_domain', 'pattern']
    ordering = ['-weight']

admin.site.register(SimpleRedirection, SimpleRedirectionAdmin)
admin.site.register(RegexRedirection, RegexRedirectionAdmin)
