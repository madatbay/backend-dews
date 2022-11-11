from rest_framework import mixins, viewsets, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer, RegisterSerializer


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


class SuggestedUserList(views.APIView):
    def get(self, request, format=None):
        users = User.objects.exclude(id__in=[request.user.id]).exclude(followers__from_user__in=[request.user])[:5]
        return Response(UserSerializer(users, many=True, context={"request": request}).data)
