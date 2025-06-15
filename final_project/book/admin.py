from django.contrib import admin
from book.models import Book, BookAuthor, BookImages, RaitingBook


admin.site.register(Book)
admin.site.register(BookAuthor)
admin.site.register(BookImages)
admin.site.register(RaitingBook)
