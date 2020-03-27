from django import forms


class MyForm(forms.Form):
    author = forms.CharField(max_length=500, required=True)
    title = forms.CharField(max_length=1000, required=True)
    goodreads_link = forms.URLField(required=False)
