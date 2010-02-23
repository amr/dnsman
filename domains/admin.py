from dnsman.domains.models import Domain
from dnsman.redirections.models import Redirection
from django.contrib import admin

class RedirectionInline(admin.TabularInline):
    model = Redirection
    extra = 2

class DomainAdmin(admin.ModelAdmin):
    inlines = [RedirectionInline]
    list_display = ('name', 'redirection_rules')
    search_fields = ['name']

admin.site.register(Domain, DomainAdmin)
