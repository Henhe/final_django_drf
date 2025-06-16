from string import digits

from django.db import models
from settings.models import Timestamp
from user.models import User
from author.models import Author
from genre.models import Genre
from django.db.models.signals import pre_delete, pre_save
from django.dispatch.dispatcher import receiver


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


class BookImages(Timestamp):
    book = models.ForeignKey(Book, verbose_name='Book', related_name='image', on_delete=models.CASCADE)
    image = models.ImageField('Image', upload_to='images')


class RaitingBook(Timestamp):
    book = models.ForeignKey(Book, verbose_name='Book', related_name='raitingbook', on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="raitingcreator")
    raiting = models.IntegerField()

    def __str__(self):
        return f'Book {self.book} creator {self.creator} raiting {self.raiting}'


class FavoriteBook(Timestamp):
    book = models.ForeignKey(Book, verbose_name='Book', related_name='favoritebook', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favoriteuser")

    def __str__(self):
        return f'Book {self.book} user {self.creator} '


@receiver(pre_delete, sender=BookImages)
def image_model_delete(sender, instance, **kwargs):
    if instance.image.name:
        instance.image.delete(False)



