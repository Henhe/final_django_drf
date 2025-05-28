from django_filters import FilterSet, ChoiceFilter
from user.models import UserRole, User


ROLE_CHOICES = (
    (UserRole.ADMIN.value, "Admin"),
    (UserRole.LIBRARIAN.value, "Librarian"),
    (UserRole.READER.value, "Reader"),
)


class UserFilterSet(FilterSet):
    role = ChoiceFilter(choices=ROLE_CHOICES, help_text="Used to filter users by role")

    class Meta:
        model = User
        fields = ("is_active", "role")
