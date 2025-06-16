from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.response import Response

from book.models import Book, BookAuthor, BookImages, RaitingBook, FavoriteBook
from book.serializers import (BookSerializer, BookSimpleSerializer,
                              BookAuthorSerializer, RaitingBookSerializer,
                              FavoriteBookSerializer)
from rest_framework.views import APIView


class BookViewSet(generics.ListAPIView, generics.CreateAPIView):
    # search_fields = ("name", "isbn", "genre__name", "bookauthor__name")
    search_fields = ("name", "isbn", "genre__name", "bookauthor__author__name")
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    ordering = ("-genre__name", )
    # ordering_fields = ("name", "isbn", "genre__name", "bookauthor__name")
    ordering_fields = ("name", "isbn", "genre__name", "bookauthor__author__name")
    filterset_fields = ["name", "isbn"]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        qp = self.request.query_params
        filter_value = qp.get('name', None)
        if filter_value is not None:
            self.queryset.filter(name__icontains=filter_value)

        filter_value = qp.get('isbn', None)
        if filter_value is not None:
            self.queryset.filter(isbn__icontains=filter_value)

        filter_value = qp.get('genre__name', None)
        if filter_value is not None:
            self.queryset.filter(genre__name__icontains=filter_value)

        filter_value = qp.get('author__name', None)
        if filter_value is not None:
            self.queryset.filter(book__author__name__icontains=filter_value)

        return self.queryset

    def post(self, request):
        data = request.data
        data['creator'] = request.user.id
        serializer = BookSimpleSerializer(data=request.data)
        if serializer.is_valid():
            book = serializer.save()
            print(f'{book=}')
            if book is not None:
                datalocal = {}
                for i in data['authors']:
                    datalocal['book'] = book.id
                    datalocal['author'] = i
                    serializer_ = BookAuthorSerializer(data=datalocal)
                    if serializer_.is_valid():
                        serializer_.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailViewSet(APIView):
    def get(self, request, id_):
        try:
            book = Book.objects.get(id=id_)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id_):
        try:
            book = Book.objects.get(id=id_)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookSimpleSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()

            BookAuthor.objects.filter(book=book).delete()
            datalocal = {}
            for i in request.data['authors']:
                datalocal['book'] = book.id
                datalocal['author'] = i
                serializer_ = BookAuthorSerializer(data=datalocal)
                if serializer_.is_valid():
                    serializer_.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, id_):
        try:
            book = Book.objects.get(id=id_)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookSimpleSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()

            BookAuthor.objects.filter(book=book).delete()
            datalocal = {}
            for i in request.data['authors']:
                datalocal['book'] = book.id
                datalocal['author'] = i
                serializer_ = BookAuthorSerializer(data=datalocal)
                if serializer_.is_valid():
                    serializer_.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id_):
        try:
            book = Book.objects.get(id=id_)
            book.delete()

        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UploadBookImage(APIView):
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)

    def put(self, request, id_):
        file_obj = request.FILES['file']

        try:
            book = Book.objects.get(id=id_)

        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        BookImages.objects.filter(book_id=book.id).delete()
        BookImages.objects.create(
            book_id=book.id,
            image=file_obj
        )

        return Response(status=204)


class RaitingBookViewSet(APIView):
    queryset = RaitingBook.objects.all()
    serializer_class = RaitingBookSerializer

    def get(self, request):
        raitings = RaitingBook.objects.all()
        serializer = RaitingBookSerializer(raitings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, id_):
        data = request.data
        data['creator'] = request.user.id

        try:
            book = Book.objects.get(id=id_)

        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        data['book'] = book.id

        serializer = RaitingBookSerializer(data=data)
        if serializer.is_valid():
            RaitingBook.objects.filter(creator=data['creator']).filter(book=book.id).delete()
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FavoriteBookDetailViewSet(APIView):
    def get(self, request):
        favoritebooks = FavoriteBook.objects.all()
        serializer = FavoriteBookSerializer(favoritebooks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        data['user'] = request.user.id
        #
        # try:
        #     book = Book.objects.get(id=id_)
        #
        # except Book.DoesNotExist:
        #     return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        #
        # data['book'] = book.id
        fb = FavoriteBook.objects.filter(book=data['book']).filter(user=request.user.id).exists()

        serializer = FavoriteBookSerializer(data=data)
        if serializer.is_valid() and not fb:
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        data = request.data
        data['user'] = request.user.id

        # try:
        #     book = Book.objects.get(id=id_)
        #
        # except Book.DoesNotExist:
        #     return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        # data['book'] = book.id
        fb = FavoriteBook.objects.filter(book=data['book']).filter(user=request.user.id)
        if fb:
            fb.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)