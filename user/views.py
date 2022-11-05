from django.contrib.auth import get_user_model

from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import UserSerializer, RegisterSerializer

User = get_user_model()


class UserViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return RegisterSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ["retrieve", "update"]:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [AllowAny]
        return super(UserViewSet, self).get_permissions()

    def get_object(self):
        return self.request.user
