from settings.permissions import CustomBasePermission
from settings.permissions import DjangoViewAction


class GenrePermission(CustomBasePermission):
    allowed_actions = DjangoViewAction.values()



