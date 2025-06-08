from genre.views import GenreViewSet, GenreDetailViewSet
from django.urls import path

urlpatterns = [
    path("", GenreViewSet.as_view(), name='genre-list-create'),
    path("<int:id_>/", GenreDetailViewSet.as_view(), name='genre-detail'),
        ]
