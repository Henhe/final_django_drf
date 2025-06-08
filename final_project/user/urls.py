from user.views import UserViewSet, TokenAuthView, RegisterView
from rest_framework.routers import SimpleRouter
from django.urls import path


router = SimpleRouter()
router.register("users", UserViewSet)
# router_contacts = SimpleRouter()


urlpatterns = [
    path("token-auth/", TokenAuthView.as_view(), name="token-auth"),
    path("register/", RegisterView.as_view(), name="register"),
    # path("activate/", UserActivationView.as_view(), name="activate"),
    # path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),
    # path("confirm-password-reset/", ConfirmPasswordReset.as_view(), name="confirm-password-reset"),
    # path("edit-password/", EditPasswordView.as_view(), name="edit-password"),
] + router.urls
