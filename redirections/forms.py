from django import forms
from dnsman.redirections.models import Redirection

class RedirectionForm(forms.ModelForm):
    class Meta:
        model = Redirection

    def clean(self):
        cleaned_data = super(RedirectionForm, self).clean()

        from_domain = cleaned_data.get('from_domain')
        to_domain = cleaned_data.get('to_domain')

        # Make sure the redirection isn't pointing to itself
        if from_domain == to_domain:
            raise forms.ValidationError('Invalid redirect from a domain to itself')
