from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from book.models import Book, BookAuthor
from author.models import Author
from author.serializers import AuthorSerializer

class BookSerializer(ModelSerializer):

    authors = serializers.SerializerMethodField()
    class Meta:
        model = Book
        fields = ('name', 'isbn', 'genre', 'authors')

    def get_authors(self, obj):
        queryset = BookAuthor.objects.filter(book=obj).values_list('author', flat=True)
        return AuthorSerializer(Author.objects.filter(id__in=queryset), many=True).data

#
# class BookSerializerSave(ModelSerializer):
#     authors = AuthorSerializer(many=True, read_only=True)
#     class Meta:
#         model = Book
#         fields = ('name', 'isbn', 'genre', 'authors')


class BookSimpleSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'name', 'isbn', 'genre', 'creator')


class BookAuthorSerializer(ModelSerializer):
    class Meta:
        model = BookAuthor
        fields = ('book', 'author')
