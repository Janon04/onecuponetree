from django import forms

class PublicationDownloadRequestForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100)
    email = forms.EmailField(label='Your Email')
    reason = forms.CharField(label='Reason for Request', widget=forms.Textarea, required=False)
