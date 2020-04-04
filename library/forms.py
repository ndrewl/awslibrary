import re
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from library.models import Book

# Maximum allowed file size in MB
MAX_BOOK_FILE_SIZE = 100


def validate_file_size(value):
    limit = MAX_BOOK_FILE_SIZE * 1024 * 1024
    if value.size > limit:
        raise ValidationError(
            f"File is too large. Maximum allowed size is {MAX_BOOK_FILE_SIZE} MB."
        )


class NewBookForm(forms.Form):
    author = forms.CharField(label="Автор", max_length=500, required=True)
    title = forms.CharField(label="Название", max_length=1000, required=True)
    language = forms.ChoiceField(
        label="Язык", choices=Book.LanguageChoice.choices, required=True
    )
    goodreads_link = forms.URLField(label="Ссылка на Goodreads", required=False)
    file = forms.FileField(
        label="Файл (желательно epub)", validators=[validate_file_size]
    )


class RegistrationForm(forms.Form):
    username = forms.CharField(label="Логин", max_length=30)
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Пароль (снова)", widget=forms.PasswordInput())

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
