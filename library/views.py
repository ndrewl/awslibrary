from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from library.models import Author, Book, BookLink, Profile
from library.forms import NewBookForm, RegistrationForm
from django.shortcuts import redirect


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password1"],
            )
            Profile.objects.create(user=user)
            return redirect("mybooks")
        else:
            return render(request, "registration/register.html", {"form": form},)

    return render(request, "registration/register.html", {"form": RegistrationForm()})


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
    context = {
        "books": Book.objects.filter(
            review_status=Book.ReviewStatusChoice.REVIEW_ACCEPTED
        ).order_by("-id")
    }
    return render(request, "library/allbooks.html", context)


@login_required
def book(request, id):
    book = Book.objects.get(id=id)
    user = User.objects.get(id=request.user.id)
    context = {
        "book": book,
        "is_in_my_books": BookLink.objects.filter(book=book, user=user).exists(),
    }
    return render(request, "library/book.html", context)


@login_required
def addbook(request, id):
    book = Book.objects.get(id=id)
    user = User.objects.get(id=request.user.id)
    link = BookLink(book=book, user=user)
    link.save()
    return redirect("mybooks")


@login_required
def delbook(request, id):
    book = Book.objects.get(id=id)
    user = User.objects.get(id=request.user.id)
    link = BookLink.objects.get(book=book, user=user)
    link.delete()
    return redirect("mybooks")


class NewBook(View):
    form_class = NewBookForm
    template_name = "library/newbook.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.get(id=request.user.id)
            author, created = Author.objects.get_or_create(
                name=form.cleaned_data["author"],
            )
            newBook = Book(
                author=author,
                title=form.cleaned_data["title"],
                goodreads_link=form.cleaned_data["goodreads_link"],
                uploaded_by=user
            )
            newBook.save()
            newBook.file = request.FILES["file"],
            newBook.save()
            newLink, created = BookLink.objects.get_or_create(book=newBook, user=user)
            return redirect("book", id=newBook.id)
        return render(request, self.template_name, {"form": form})

