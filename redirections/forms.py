from django import forms
from dnsman.redirections.models import Redirection
from dnsman.domains.models import Domain

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

class RedirectionBulkAdd(forms.Form):
    to_domain = forms.ModelChoiceField(Domain.objects.all(), help_text='The domain to redirect to')
    from_domains = forms.CharField(widget=forms.Textarea, help_text='The domains that will redirect to the selected domain. One domain per line. Domains that do not exist already will be automatically created. Do not include www')
    ignore_errors = forms.BooleanField(required=False, help_text='If checked, then errors will be ignored and reported at the end, and the successfully imported domains will be automatically removed from the text area')
