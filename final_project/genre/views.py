from importlib.metadata import requires

from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.views import APIView
from genre.models import Genre
from genre.serializers import GenreSerializer
from settings.views import CustomModelViewSet, CustomAPIView

class GenreViewSet(APIView):
    search_fields = ("name")
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    ordering = ("-id", )
    ordering_fields = ("name")
    filterset_fields = ["name"]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


    def get_queryset(self):
        qp = self.request.query_params
        filter_value = qp.get('name', None)

        if filter_value is not None:
            self.queryset.filter(name__icontains=filter_value)

        return self.queryset
    # def get(self, request):
    #     genre = Genre.objects.all()
    #     serializer = GenreSerializer(genre, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        data['creator'] = request.user.id
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenreDetailViewSet(APIView):

    def get(self, request, id_):
        try:
            genre = Genre.objects.get(id=id_)
        except Genre.DoesNotExist:
            return Response({"error": "Genre not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = GenreSerializer(genre)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id_):
        try:
            author = Genre.objects.get(id=id_)
        except Genre.DoesNotExist:
            return Response({"error": "Genre not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = GenreSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, id_):
        try:
            genre = Genre.objects.get(id=id_)
        except Genre.DoesNotExist:
            return Response({"error": "Genre not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = GenreSerializer(genre, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id_):
        try:
            genre = Genre.objects.get(id=id_)
            genre.delete()

        except Genre.DoesNotExist:
            return Response({"error": "Genre not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


