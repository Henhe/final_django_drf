from book.views import BookViewSet, BookDetailViewSet, UploadBookImage, RaitingBookViewSet
from django.urls import path


urlpatterns = ([
        path("", BookViewSet.as_view(), name='book-list-create'),
        path("<int:id_>/", BookDetailViewSet.as_view(), name='book-detail'),
        path("cover/<int:id_>/", UploadBookImage.as_view(), name='book-cover'),
        path("raiting/<int:id_>/", RaitingBookViewSet.as_view(), name='book-raiting'),
        ]
        )

