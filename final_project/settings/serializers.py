from rest_framework.serializers import Serializer, CharField


class ErrorSerializer(Serializer):
    error = CharField(read_only=True)


class DetailSerializer(Serializer):
    detail = CharField(read_only=True)
