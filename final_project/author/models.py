from django.db import models
from settings.models import Timestamp
from user.models import User


class Country(Timestamp, models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contry_creator")

    def __str__(self):
        return self.name

class Author(Timestamp, models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    birth_year = models.IntegerField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="author_country")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_creator")
    # books = relationship(Book, back_populates="author")

    def __str__(self):
        return f'Author {self.name} born {self.birth_year} country {self.country.name}'
