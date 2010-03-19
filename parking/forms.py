from django import forms
from django.template.defaultfilters import slugify
from django.conf import settings
from dnsman.parking.models import ParkingPage
import zipfile, os

class ParkingPageForm(forms.ModelForm):
    template_file = forms.FileField(label='Or upload it', required=False, help_text='Work offline in your favorite editor, and upload the template file here')
    resources_dir = forms.FileField(label='Zip archive', required=False, help_text='Upload a .zip file containing the external resources, relative to your XHTML template')

    class Meta:
        model = ParkingPage

    def clean_template_file(self):
        f = self.cleaned_data['template_file']
        if f is not None:
            if not f.content_type.startswith('text'):
                raise forms.ValidationError('Uploaded file must be plain text (.html, .txt, etc)')
        return f

    def clean_resources_dir(self):
        f = self.cleaned_data['resources_dir']
        if f is not None:
            ext = os.path.splitext(f.name)[1]
            if ext != '.zip' or f.content_type != 'application/zip':
                raise forms.ValidationError('Uploaded file must be a valid Zip archive')
        return f

    def clean(self):
        self.cleaned_data = super(ParkingPageForm, self).clean()

        # Template file
        if self.cleaned_data.has_key('template_file') and self.cleaned_data['template_file'] is not None:
            self.cleaned_data['template'] = unicode(self.cleaned_data['template_file'].read())

        # External resources file
        if self.cleaned_data.has_key('resources_dir') and self.cleaned_data['resources_dir'] is not None:
            f = self.cleaned_data['resources_dir']

            try:                
                z = zipfile.ZipFile(f)
            
                if z.testzip() is not None:
                    raise zipfile.BadZipFile()

                slug = slugify(self.cleaned_data['name'])
                resources_dir = os.path.join(settings.PARKING_PAGES_DIR, slug)
                os.mkdir(resources_dir)

                # TODO: Need more validation
                # See: http://docs.python.org/library/zipfile.html#zipfile.ZipFile.extractall
                z.extractall(resources_dir)
                self.cleaned_data['resources_dir'] = resources_dir
            except Exception, e:
                print e
                raise forms.ValidationError('Could not unzip the uploaded file')

        return self.cleaned_data
