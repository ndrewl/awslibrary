import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Author(models.Model):
    name = models.CharField(max_length=500, blank=False)

    def __str__(self):
        return self.name


def _get_updload_file_path(instance, filename):
    return os.path.join(str(instance.id), filename)


class Book(models.Model):
    class ReviewStatusChoice(models.TextChoices):
        REVIEW_PENDING = "Pending", _("Pending")
        REVIEW_ACCEPTED = "Accepted", _("Accepted")
        REVIEW_REJECTED = "Rejected", _("Rejected")

    class LanguageChoice(models.TextChoices):
        RUSSIAN = "Russian", _("Russian")
        ENGLISH = "English", _("English")
        FRENCH = "French", _("French")

    title = models.CharField(max_length=1000, blank=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    goodreads_link = models.URLField(blank=True)
    file = models.FileField(null=True, blank=True, upload_to=_get_updload_file_path)
    review_status = models.CharField(
        choices=ReviewStatusChoice.choices,
        max_length=100,
        default=ReviewStatusChoice.REVIEW_PENDING,
    )
    uploaded_by = models.ForeignKey(
        User, related_name="uploaded_by", on_delete=models.SET_NULL, null=True
    )
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    language = models.CharField(
        choices=LanguageChoice.choices, max_length=100, null=True
    )

    def __str__(self):
        return f"{self.author.name} - {self.title}"


class BookLink(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.book}"
