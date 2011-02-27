from django import forms
from django.conf import settings
from django.utils.encoding import force_unicode, DjangoUnicodeDecodeError

from django.forms.util import ErrorList

from dnsman.zones.models import Zone

class ZoneAddForm(forms.ModelForm):
    class Meta:
        model = Zone
        fields = ('domain',)

class ZoneChangeForm(forms.ModelForm):
    definition = forms.CharField(label='Definition',
                                 widget=forms.Textarea(attrs={'class': 'vLargeTextField', 'rows': '20'}),
                                 required=True, help_text='The zone definition (the contents of the zone file)')

    class Meta:
        model = Zone

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        if initial is None:
            initial = {}

        if instance is not None:
            initial['definition'] = instance.definition
        
        super(ZoneChangeForm, self).__init__(data, files, auto_id, prefix,
                 initial, error_class, label_suffix,
                 empty_permitted, instance)

    def save(self, commit=True):
        result = super(forms.ModelForm, self).save(commit)
        result.definition = self.cleaned_data['definition']
        return result
