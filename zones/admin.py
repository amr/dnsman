from django.contrib import admin
from django.utils.functional import curry
from django.forms.models import modelform_factory, modelformset_factory, inlineformset_factory

from dnsman.zones.models import Zone
from dnsman.zones.forms import ZoneChangeForm, ZoneAddForm

class ZoneAdmin(admin.ModelAdmin):
    add_form = ZoneAddForm
    change_form = ZoneChangeForm

    list_display = ('domain', 'formatted_last_modified')
    list_filter = ['domain']
    search_fields = ['domain']

    # We override this to give different forms for add and change
    def get_form(self, request, obj=None, **kwargs):
        try:
            if obj is None:
                form = self.add_form
            else:
                form = self.change_form
        except AttributeError:
            raise ImproperlyConfigured("%s must have add_form and change_form defined" % self.__name__)
        
        if self.declared_fieldsets:
            fields = flatten_fieldsets(self.declared_fieldsets)
        else:
            fields = None
        if self.exclude is None:
            exclude = []
        else:
            exclude = list(self.exclude)
        exclude.extend(kwargs.get("exclude", []))
        exclude.extend(self.get_readonly_fields(request, obj))
        # if exclude is an empty list we pass None to be consistant with the
        # default on modelform_factory
        exclude = exclude or None
        defaults = {
            "form": form,
            "fields": fields,
            "exclude": exclude,
            "formfield_callback": curry(self.formfield_for_dbfield, request=request),
        }
        defaults.update(kwargs)
        return modelform_factory(self.model, **defaults)

    def get_afieldsets(self, request, obj=None):
        if obj is None:
            return self.add_fieldsets
        else:
            return self.change_fieldsets


admin.site.register(Zone, ZoneAdmin)
