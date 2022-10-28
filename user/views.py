from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.contrib.auth.models import User

from .serializers import UserSerializer, RegisterSerializer


class UserViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return RegisterSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ["create"]:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super(UserViewSet, self).get_permissions()

    def get_object(self):
        return self.request.user
