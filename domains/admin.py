from dnsman.domains.models import Domain
from dnsman.redirections.models import SimpleRedirection, RegexRedirection
from django.contrib import admin

class SimpleRedirectionInline(admin.TabularInline):
    model = SimpleRedirection
    extra = 1
    fk_name = 'to_domain'
    fields = ['from_domain', 'full_uri', 'code']
    ordering = ['-weight']

class RegexRedirectionInline(admin.TabularInline):
    model = RegexRedirection
    extra = 1
    fk_name = 'to_domain'
    fields = ['pattern', 'full_uri', 'code']
    ordering = ['-weight']

class DomainAdmin(admin.ModelAdmin):
    list_display = ('name', 'redirections_count')
    search_fields = ['name']

admin.site.register(Domain, DomainAdmin)
