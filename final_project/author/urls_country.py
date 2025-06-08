from author.views import CountryViewSet, CountryDetailViewSet
from django.urls import path

urlpatterns = (
    [
        path("", CountryViewSet.as_view(), name='country-list-create'),
        path("<int:id_>/", CountryDetailViewSet.as_view(), name='country-detail'),
    ]
               )

