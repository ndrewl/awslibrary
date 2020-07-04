from functools import wraps
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from library.models import Author, Book, BookLink, Profile
from library.forms import NewBookForm, RegistrationForm


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


def user_has_permission(permission):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            profile = Profile.objects.get(user=request.user)
            if permission == "download" and not profile.can_download_books:
                return render(request, "library/nopermission.html")

            if permission == "upload" and not profile.can_upload_books:
                return render(request, "library/nopermission.html")

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


@login_required
@user_has_permission("download")
def mybooks(request):
    book_links = BookLink.objects.filter(user__id=request.user.id)
    language = request.GET.get("language", None)
    if language is not None:
        book_links = book_links.filter(book__language=language)

    context = {"books": [link.book for link in book_links.order_by("-id")]}
    return render(request, "library/mybooks.html", context)


@login_required
@user_has_permission("download")
def allbooks(request):
    books = Book.objects.filter(review_status=Book.ReviewStatusChoice.REVIEW_ACCEPTED)
    language = request.GET.get("language", None)
    if language is not None:
        books = books.filter(language=language)

    context = {"books": books.order_by("-id")}
    return render(request, "library/allbooks.html", context)


def book(request, id):
    book = Book.objects.get(id=id)

    full_info_visible = False
    download_links_visible = False
    in_my_books = None

    if request.user.is_authenticated:
        full_info_visible = True
        profile = Profile.objects.get(user=request.user)
        download_links_visible = profile.can_download_books
        in_my_books = BookLink.objects.filter(book=book, user=request.user).exists()

    context = {
        "book": book,
        "full_info_visible": full_info_visible,
        "download_links_visible": download_links_visible,
        "in_my_books": in_my_books,
    }

    return render(request, "library/book.html", context)


@login_required
@user_has_permission("download")
def addbook(request, id):
    book = Book.objects.get(id=id)
    user = User.objects.get(id=request.user.id)
    link = BookLink(book=book, user=user)
    link.save()
    return redirect("mybooks")


@login_required
@user_has_permission("download")
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
    @method_decorator(user_has_permission("upload"))
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
                uploaded_by=user,
                language=form.cleaned_data["language"],
            )
            newBook.save()
            newBook.file = request.FILES["file"]
            newBook.save()
            newLink, created = BookLink.objects.get_or_create(book=newBook, user=user)
            return redirect("book", id=newBook.id)
        return render(request, self.template_name, {"form": form})

