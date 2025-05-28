from settings.enums import CustomEnum


class DjangoViewAction(CustomEnum):
    LIST = "list"
    CREATE = "create"
    UPDATE = "update"
    RETRIEVE = "retrieve"
    PARTIAL_UPDATE = "partial_update"
    DELETE = "destroy"


class DjangoHttpMethod(CustomEnum):
    POST = "POST"
    GET = "GET"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


HTTP_METHODS_ACTIONS_MAP = {
    DjangoHttpMethod.POST.value: DjangoViewAction.CREATE.value,
    DjangoHttpMethod.GET.value: DjangoViewAction.LIST.value,
    DjangoHttpMethod.PUT.value: DjangoViewAction.UPDATE.value,
    DjangoHttpMethod.PATCH.value: DjangoViewAction.PARTIAL_UPDATE.value,
    DjangoHttpMethod.DELETE.value: DjangoViewAction.DELETE.value,
}
