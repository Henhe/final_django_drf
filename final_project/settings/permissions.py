from rest_framework.permissions import BasePermission
from user.models import User
from settings.constants import DjangoViewAction


class CustomBasePermission(BasePermission):
    allowed_actions = DjangoViewAction.values()

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.user.is_staff:
            return True
        if view.action in self.allowed_actions:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if (
            request.user.is_staff
            or (isinstance(obj, User) and request.user == obj)
            or (hasattr(obj, "user") and obj.user == request.user)
            or (hasattr(obj, "contact") and obj.contact == request.user)
        ):
            return True
        return False
