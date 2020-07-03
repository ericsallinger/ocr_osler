from django import forms

class JoinForm(forms.Form):  # or forms.ModelForm
    name = forms.CharField(max_length=120)
