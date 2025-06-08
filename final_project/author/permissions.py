from settings.permissions import CustomBasePermission
from settings.constants import DjangoViewAction
# from settings.permissions import DjangoViewAction
from rest_framework.permissions import BasePermission
from author.models import Country, Author
from user.models import User

class CountryPermission(CustomBasePermission):
    allowed_actions = DjangoViewAction.values()

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        # if not request.user.is_active:
        #     return True
        if view.action in self.allowed_actions:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # if (
        #     (isinstance(obj, User) and request.user == obj)
        #     or (hasattr(obj, "user") and obj.user == request.user)
        # ):
        #     return True
        # return False

        if not (request.user and request.user.is_authenticated):
            return False
        return True


class AuthorPermission(CustomBasePermission):
    allowed_actions = DjangoViewAction.values()
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        # if not request.user.is_active:
        #     return True
        if view.action in self.allowed_actions:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if not (request.user and request.user.is_authenticated):
            return False
        return True

# class FundsPermission(CustomBasePermission):
#     allowed_actions = DjangoViewAction.values()
#     def has_permission(self, request, view):
#         if not (request.user and request.user.is_authenticated):
#             return False
#         if request.user.is_staff:
#             return True
#         if view.action in self.allowed_actions:
#             return True
#         return False
#
#     def has_object_permission(self, request, view, obj):
#         if (
#             request.user.is_staff
#             or (isinstance(obj, User) and request.user == obj)
#             or (hasattr(obj, "user") and obj.user == request.user)
#             or (hasattr(obj, "contact") and obj.contact == request.user)
#         ):
#             return True
#         return False

# class IsCreatorOrOwnerOfBudgetExecution(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.user.is_staff:
#             return True
#         if (isinstance(obj, Funds) and obj.budget.creator == request.user
#                 or obj.creator == request.user):
#             return True
#         return False
#         # return obj.creator == request.user


