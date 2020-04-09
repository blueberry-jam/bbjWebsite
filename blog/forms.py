from django import forms 

class blogForm(forms.Form):
    body = forms.CharField(widget=forms.HiddenInput)
    title = forms.CharField(widget=forms.HiddenInput)
    description = forms.CharField(widget=forms.HiddenInput)

class deleteForm(forms.Form):
    delete = forms.CharField(widget=forms.HiddenInput)