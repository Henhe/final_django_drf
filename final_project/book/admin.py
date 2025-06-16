from django.contrib import admin
from book.models import Book, BookAuthor, BookImages, RaitingBook, FavoriteBook


admin.site.register(Book)
admin.site.register(BookAuthor)
admin.site.register(BookImages)
admin.site.register(RaitingBook)
admin.site.register(FavoriteBook)
