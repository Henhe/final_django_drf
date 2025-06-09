from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from author.models import Country, Author
from author.serializers import CountrySerializer, AuthorSerializer
from rest_framework.views import APIView


class AuthorViewSet(generics.ListAPIView, generics.CreateAPIView):
    search_fields = ("name", "country__name", "birth_year")
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    ordering = ("-id", )
    ordering_fields = ("country__name", "name", "birth_year")
    filterset_fields = ["country__name", "name", "birth_year"]
    queryset = Author.objects.all()
    serializer_class = CountrySerializer

    def get_queryset(self):
        qp = self.request.query_params
        filter_value = qp.get('country__name', None)
        if filter_value is not None:
            self.queryset.filter(country__name__icontains=filter_value)

        filter_value = qp.get('name', None)
        if filter_value is not None:
            self.queryset.filter(name__icontains=filter_value)

        filter_value = qp.get('birth_year', None)
        if filter_value is not None:
            self.queryset.filter(birth_year=filter_value)

        return self.queryset

    def post(self, request):
        data = request.data
        data['creator'] = request.user.id
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthorDetailViewSet(APIView):
    def get(self, request, id_):
        try:
            author = Author.objects.get(id=id_)
        except Author.DoesNotExist:
            return Response({"error": "Author not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AuthorSerializer(author)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id_):
        try:
            author = Author.objects.get(id=id_)
        except Author.DoesNotExist:
            return Response({"error": "Author not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, id_):
        try:
            author = Author.objects.get(id=id_)
        except Author.DoesNotExist:
            return Response({"error": "Author not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id_):
        try:
            author = Author.objects.get(id=id_)
            author.delete()

        except Author.DoesNotExist:
            return Response({"error": "Author not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CountryViewSet(generics.ListAPIView, generics.CreateAPIView):
    search_fields = ("name", )
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    ordering = ("-id", )
    ordering_fields = ("name",)
    filterset_fields = ["name"]
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    def get_queryset(self):
        qp = self.request.query_params
        filter_value=qp.get('name', None)

        if filter_value is not None:
            self.queryset.filter(name__icontains=filter_value)

        return self.queryset

    def post(self, request):
        data = request.data
        data['creator'] = request.user.id
        serializer = CountrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CountryDetailViewSet(APIView):
    def get(self, request, id_):
        try:
            country = Country.objects.get(id=id_)
        except Country.DoesNotExist:
            return Response({"error": "Country not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CountrySerializer(country)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id_):
        try:
            country = Country.objects.get(id=id_)
        except Country.DoesNotExist:
            return Response({"error": "Country not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CountrySerializer(country, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, id_):
        try:
            country = Country.objects.get(id=id_)
        except Country.DoesNotExist:
            return Response({"error": "Country not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CountrySerializer(country, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id_):
        try:
            country = Country.objects.get(id=id_)
            country.delete()

        except Country.DoesNotExist:
            return Response({"error": "Country not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)









# class ReportAPIView(APIView):
#
#     def get_permissions(self):
#         permission_classes = [IsAuthenticatedOrReadOnly]
#         return [permission() for permission in permission_classes]
#
#     def get(self, request):
#         print(f'{request.GET=}')
#         id = request.GET.get('id', '')
#         data_ = Budget.objects.filter(id=id).first()
#         if data_:
#             response = HttpResponse(content_type='text/plain')
#             response['Content-Disposition'] = 'filename="report.txt"'
#
#             buffer = BytesIO()
#             buffer.write(f'Budget: {data_}'.encode('utf-8'))
#             data_funds = Funds.objects.filter(budget__pk=id).all()
#             for i in data_funds:
#                 buffer.write(f'\nCreator: {i.creator} sum {i.sum}'.encode('utf-8'))
#
#             txt = buffer.getvalue()
#             buffer.close()
#
#             response = HttpResponse(txt, content_type='application/text charset=utf-8')
#             response['Content-Disposition'] = 'attachment; filename="report.txt"'
#             return response
#         else:
#             return Response(None, status=status.HTTP_201_CREATED)
#
#
