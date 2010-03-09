from django import forms

class DomainBulkAdd(forms.Form):
    domains = forms.CharField(widget=forms.Textarea, help_text='One domain per line')
    ignore_errors = forms.BooleanField(required=False, help_text='If checked, then errors will be ignored and reported at the end, and the successfully imported domains will be automatically removed from the text area')
