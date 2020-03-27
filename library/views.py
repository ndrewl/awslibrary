from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from library.models import Author, Book, BookLink
from library.forms import MyForm
from django.shortcuts import redirect


@login_required
def mybooks(request):
    context = {
        "books": [
            link.book
            for link in BookLink.objects.filter(user__id=request.user.id).order_by(
                "-id"
            )
        ]
    }
    return render(request, "library/mybooks.html", context)


@login_required
def allbooks(request):
    context = {"books": Book.objects.order_by("-id")}
    return render(request, "library/allbooks.html", context)


@login_required
def book(request, id):
    context = {"book": Book.objects.get(id=id)}
    return render(request, "library/book.html", context)


class NewBook(View):
    form_class = MyForm
    template_name = "library/newbook.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        print(request.POST)
        if form.is_valid():
            author, created = Author.objects.get_or_create(
                name=form.cleaned_data["author"],
            )
            newBook, created = Book.objects.get_or_create(
                author=author,
                title=form.cleaned_data["title"],
                goodreads_link=form.cleaned_data["goodreads_link"],
            )
            print(request.user.id)
            user = User.objects.get(id=request.user.id)
            print(user)
            newLink, created = BookLink.objects.get_or_create(book=newBook, user=user)
            return redirect("book", id=newBook.id)
        return render(request, self.template_name, {"form": form})

