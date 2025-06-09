from django.db import models
from settings.models import Timestamp
from user.models import User
from author.models import Author
from genre.models import Genre


class Book(Timestamp, models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    isbn = models.CharField(unique=True, max_length=13)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="book_genre")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="book_creator")

    def __str__(self):
        return f'Book {self.name} isbn {self.isbn} genre {self.genre.name}'


class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)