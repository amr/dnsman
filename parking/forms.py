from django import forms
from dnsman.parking.models import ParkingPage

class ParkingPageForm(forms.ModelForm):
    template_file = forms.FileField(label='Or upload a file', required=False, help_text='Upload your XHTML template directly')
    #resources_dir = forms.FileField(label='External resources', help_text='Upload a .zip file containing the external resources, relative to your XHTML template')

    class Meta:
        model = ParkingPage

    def clean(self):
        self.cleaned_data = super(ParkingPageForm, self).clean()

        if self.cleaned_data['template_file'] is not None:
            self.cleaned_data['template'] = unicode(self.cleaned_data['template_file'].read())
        return self.cleaned_data
