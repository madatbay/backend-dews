from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'user'

router = DefaultRouter()
router.register(r'user', views.UserViewSet, basename='user')


urlpatterns = router.urls + [
    path("suggested-users-list/", views.SuggestedUserList.as_view(), name="suggested_users_list"),
    path("update-user-followings/", views.UpdateUserFollowings.as_view(), name="update_user_followings"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
