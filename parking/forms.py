from django import forms
from dnsman.parking.models import ParkingPage

class ParkingPageForm(forms.ModelForm):
    #template = forms.FileField(help_text='Upload your XHTML template')
    #resources_dir = forms.FileField(label='External resources', help_text='Upload a .zip file containing the external resources, relative to your XHTML template')

    class Meta:
        model = ParkingPage

    #def clean_template(self):
#        pass
