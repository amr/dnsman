from dnsman.domains.models import Domain
from dnsman.redirections.models import Redirection
from django.contrib import admin

class RedirectionInline(admin.TabularInline):
    model = Redirection
    extra = 1
    fk_name = 'to_domain'
    fields = ['type', 'from_domain', 'pattern', 'full_uri', 'code']
    ordering = ['-weight']

class DomainAdmin(admin.ModelAdmin):
    inlines = [RedirectionInline]
    list_display = ('name', 'redirections_count')
    search_fields = ['name']

admin.site.register(Domain, DomainAdmin)
