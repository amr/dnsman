from django import forms
from django.template.defaultfilters import slugify
from django.conf import settings
from dnsman.parking.models import ParkingPage
from django.utils.encoding import force_unicode, DjangoUnicodeDecodeError
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
            try:
                self.cleaned_data['template'] = force_unicode(self.cleaned_data['template_file'].read())
            except DjangoUnicodeDecodeError:
                from django.forms.util import ErrorList
                self._errors['template_file'] = ErrorList(["The template file must be UTF-8 encoded"])

        return self.cleaned_data

class ParkingPageDeleteForm(forms.Form):
    keep_resources = forms.BooleanField(required=False, label="Don't delete associated external resources", help_text="foo")
