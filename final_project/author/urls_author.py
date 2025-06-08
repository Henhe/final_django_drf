from author.views import AuthorViewSet, AuthorDetailViewSet
from django.urls import path


urlpatterns = ([
       path("", AuthorViewSet.as_view(), name='author-list-create'),
       path("<int:id_>/", AuthorDetailViewSet.as_view(), name='author-detail'),
        ]
                )

