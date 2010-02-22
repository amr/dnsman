from dnsman.redirections.models import Redirection
from django.contrib import admin

class RedirectionAdmin(admin.ModelAdmin):
    list_display = ('pattern', 'full_uri', 'code')
    list_filter = ['code', 'full_uri']
    search_fields = ['domain', 'pattern']

admin.site.register(Redirection, RedirectionAdmin)
