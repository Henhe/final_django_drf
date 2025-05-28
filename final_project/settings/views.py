from rest_framework.mixins import ListModelMixin, CreateModelMixin, \
    RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from drf_yasg.utils import swagger_auto_schema
from settings.inspectors import CustomPaginationInspector
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class CustomListModelMixin(ListModelMixin):
    @swagger_auto_schema(paginator_inspectors=[CustomPaginationInspector])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CustomGenericViewSet(GenericViewSet):
    possible_errors_map = {
        "create": (status.HTTP_401_UNAUTHORIZED, status.HTTP_400_BAD_REQUEST, status.HTTP_403_FORBIDDEN),
        "list": (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        "retrieve": (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND),
        "update": (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND, status.HTTP_400_BAD_REQUEST),
        "partial_update": (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND, status.HTTP_400_BAD_REQUEST),
        "destroy": (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND),
    }


class CustomModelViewSet(
    CustomListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    CustomGenericViewSet
):
    pass


class CustomAPIView(APIView):
    response_serializer = None
    request_serializer = None
    tags = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = None

    def response(self, data=None, http_status=status.HTTP_200_OK, message=None):
        response = {"data": data or self.data}

        if message:
            response["detail"] = message

        return Response(data=response, status=http_status)

    # def post_related_operations(self, request) -> dict:
    #     pass
    #
    # @swagger_auto_schema(
    #     request_body=request_serializer() if request_serializer else None,
    #     responses={
    #         status.HTTP_200_OK: response_serializer() if response_serializer else None,
    #         # status.HTTP_400_BAD_REQUEST: ErrorSerializer(),
    #         # status.HTTP_404_NOT_FOUND: ErrorSerializer(),
    #     },
    #     tags=tags
    # )
    # def post(self, request):
    #     self.data = self.post_related_operations(request)
    #     return self.response()
