from rest_framework.serializers import ModelSerializer
from author.models import Country, Author


class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'
        # extra_kwargs = {
        #     'id': {'read_only': False},
        #     'slug': {'validators': []},
        # }

class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
