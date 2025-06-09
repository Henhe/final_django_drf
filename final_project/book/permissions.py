from settings.permissions import CustomBasePermission
from settings.constants import DjangoViewAction


class BookPermission(CustomBasePermission):
    allowed_actions = DjangoViewAction.values()

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        if view.action in self.allowed_actions:
            return True
        return False

    def has_object_permission(self, request, view, obj):

        if not (request.user and request.user.is_authenticated):
            return False
        return True


class BookAuthorPermission(CustomBasePermission):
    allowed_actions = DjangoViewAction.values()

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        if view.action in self.allowed_actions:
            return True
        return False

    def has_object_permission(self, request, view, obj):

        if not (request.user and request.user.is_authenticated):
            return False
        return True





