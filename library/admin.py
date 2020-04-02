from django.contrib import admin
from library.models import Profile, Author, Book, BookLink


class ProfileAdmin(admin.ModelAdmin):
    pass


class AuthorAdmin(admin.ModelAdmin):
    pass


def book_accept(modeladmin, request, queryset):
    queryset.update(
        review_status=Book.ReviewStatusChoice.REVIEW_ACCEPTED, reviewer=request.user.id
    )


book_accept.short_description = "Accept selected books"


def book_reject(modeladmin, request, queryset):
    queryset.update(
        review_status=Book.ReviewStatusChoice.REVIEW_REJECTED, reviewer=request.user.id
    )


book_reject.short_description = "Reject selected books"


class BookAdmin(admin.ModelAdmin):
    list_display = ("author", "title", "uploaded_by", "review_status")
    list_filter = ("review_status", "reviewer")
    actions = (book_accept, book_reject)


class BookLinkAdmin(admin.ModelAdmin):
    pass


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookLink, BookLinkAdmin)
