from django.shortcuts import render
from library.models import Book


def index(request):
    context = {"books": Book.objects.order_by("-id")}
    return render(request, "library/index.html", context)
