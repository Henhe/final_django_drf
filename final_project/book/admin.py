from django.contrib import admin
from book.models import Book, BookAuthor


admin.site.register(Book)
admin.site.register(BookAuthor)