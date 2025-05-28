from settings.permissions import CustomBasePermission
from settings.constants import DjangoViewAction


class UserPermission(CustomBasePermission):
    allowed_actions = DjangoViewAction.values(exclude=[DjangoViewAction.CREATE])


class ContactPermission(CustomBasePermission):
    allowed_actions = DjangoViewAction.values(exclude=[DjangoViewAction.UPDATE])
