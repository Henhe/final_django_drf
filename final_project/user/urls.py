from user.views import UserViewSet, TokenAuthView, RegisterView
from rest_framework.routers import SimpleRouter
from django.urls import path


router = SimpleRouter()
router.register("users", UserViewSet)


urlpatterns = [
    path("token-auth/", TokenAuthView.as_view(), name="token-auth"),
    path("register/", RegisterView.as_view(), name="register"),
] + router.urls
