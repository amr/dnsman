from django import forms
from django.template.defaultfilters import slugify
from django.conf import settings
from dnsman.parking.models import ParkingPage
import zipfile, os

class ParkingPageAddForm(forms.ModelForm):
    class Meta:
        model = ParkingPage
        fields = ('name', 'resources_dir')

class ParkingPageChangeForm(forms.ModelForm):
    template_file = forms.FileField(label='Or upload it', required=False, help_text='Work offline in your favorite editor, and upload the template file here')

    class Meta:
        model = ParkingPage

    def clean_template_file(self):
        f = self.cleaned_data['template_file']
        if f is not None:
            if not f.content_type.startswith('text'):
                raise forms.ValidationError('Uploaded file must be plain text (.html, .txt, etc)')
        return f

    def clean(self):
        self.cleaned_data = super(ParkingPageChangeForm, self).clean()

        # Template file
        if self.cleaned_data.has_key('template_file') and self.cleaned_data['template_file'] is not None:
            self.cleaned_data['template'] = unicode(self.cleaned_data['template_file'].read())

        return self.cleaned_data
