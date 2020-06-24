from django import forms

class JoinForm(forms.Form):  # or forms.ModelForm
    email = forms.EmailField()
    name = forms.CharField(max_length=120)
