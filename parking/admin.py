from django.contrib import admin

from dnsman.parking.models import ParkingPage
from dnsman.parking.forms import ParkingPageForm

class ParkingPageAdmin(admin.ModelAdmin):
    form = ParkingPageForm
    fieldsets = [
        ('Template', {'fields': ['template', 'template_file'], 'classes': ['template']}),
        ('External resources', {'fields': ['resources_dir'], 'classes': ['collapse', 'external-resources'], 'description': 'Upload files used by the parking page (stylesheets, images, etc). Upload a .zip file and it will be automatically unpacked where you uploaded it.'}),
        ('Advanced', {'fields': ['extends'], 'classes': ['collapse', 'advanced']}),
    ]
    list_display = ('name', 'extends', 'last_modified')
    list_filter = ['extends']
    search_fields = ['name']

admin.site.register(ParkingPage, ParkingPageAdmin)
