from django import forms
import re
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User


class NewBookForm(forms.Form):
    author = forms.CharField(max_length=500, required=True)
    title = forms.CharField(max_length=1000, required=True)
    goodreads_link = forms.URLField(required=False)
    file = forms.FileField()


class RegistrationForm(forms.Form):
    username = forms.CharField(label="Username", max_length=30)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Password (Again)", widget=forms.PasswordInput())

    def clean_password2(self):
        if "password1" in self.cleaned_data:
            password1 = self.cleaned_data["password1"]
            password2 = self.cleaned_data["password2"]
            if password1 == password2:
                return password2
        raise forms.ValidationError("Passwords do not match.")

    def clean_username(self):
        username = self.cleaned_data["username"]
        if not re.search(r"^\w+$", username):
            raise forms.ValidationError(
                "Username can only contain alphanumeric characters and the underscore."
            )
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError("Username is already taken.")
