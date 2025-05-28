from drf_yasg.inspectors import PaginatorInspector, SwaggerAutoSchema
from drf_yasg import openapi
from settings.constants import HTTP_METHODS_ACTIONS_MAP, DjangoHttpMethod, DjangoViewAction
from settings.serializers import ErrorSerializer


class CustomPaginationInspector(PaginatorInspector):
    def get_paginated_response(self, paginator, response_schema):
        schema = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "meta": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "count": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "page": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "perPage": openapi.Schema(type=openapi.TYPE_INTEGER),
                    },
                ),
                "data": response_schema,
            }
        )

        return schema


class CustomSwaggerAutoSchema(SwaggerAutoSchema):
    def get_action(self):
        action = HTTP_METHODS_ACTIONS_MAP.get(self.method)

        if self.method == DjangoHttpMethod.GET.value and not self.is_list_view():
            action = DjangoViewAction.RETRIEVE.value

        return action

    def get_default_responses(self):
        responses = super().get_default_responses()

        if hasattr(self.view, "possible_errors_map"):
            action = self.get_action()
            for error in self.view.possible_errors_map.get(action, []):
                responses.update({error: ErrorSerializer()})

        return responses

    def get_request_serializer(self):
        from config.views import CustomAPIView
        serializer = super().get_request_serializer()

        if issubclass(self.view.__class__, CustomAPIView):
            return self.view.request_serializer()

        return serializer

    def get_default_response_serializer(self):
        from config.views import CustomAPIView
        serializer = super().get_default_response_serializer()

        if issubclass(self.view.__class__, CustomAPIView):
            return self.view.response_serializer()

        return serializer

    def get_tags(self, operation_keys=None):
        tags = super().get_tags(operation_keys)

        if hasattr(self.view, "tags") and self.view.tags:
            return self.view.tags

        return tags
