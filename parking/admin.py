from django.contrib import admin

from dnsman.parking.models import ParkingPage
from dnsman.parking.forms import ParkingPageForm

class ParkingPageAdmin(admin.ModelAdmin):
    form = ParkingPageForm
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Template', {'fields': ['template', 'extends', 'resources_dir']}),
    ]
    list_display = ('name', 'extends', 'last_modified')
    list_filter = ['extends']
    search_fields = ['name']

admin.site.register(ParkingPage, ParkingPageAdmin)
