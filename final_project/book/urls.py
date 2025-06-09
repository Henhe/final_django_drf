from book.views import BookViewSet, BookDetailViewSet
from django.urls import path


urlpatterns = ([
       path("", BookViewSet.as_view(), name='book-list-create'),
       path("<int:id_>/", BookDetailViewSet.as_view(), name='book-detail'),
        ]
                )

