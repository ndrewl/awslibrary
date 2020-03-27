from django.contrib import admin
from library.models import Profile, Author, Book, BookLink


class ProfileAdmin(admin.ModelAdmin):
    pass


class AuthorAdmin(admin.ModelAdmin):
    pass


class BookAdmin(admin.ModelAdmin):
    pass

class BookLinkAdmin(admin.ModelAdmin):
    pass


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookLink, BookLinkAdmin)
