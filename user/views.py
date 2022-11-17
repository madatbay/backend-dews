from rest_framework import mixins, viewsets, views, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import User, FollowRelation
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


class UpdateUserFollowings(views.APIView):
    def post(self, request, format=None):
        action = request.data.get("action")
        user_id = request.data.get("user_id")

        if not any([action, user_id]):
            return Response({"detail": "Both fields are required. action, user_id"}, status=status.HTTP_400_BAD_REQUEST)

        if action not in ["follow", "unfollow"]:
            return Response({"detail": "Incorrect option for action. Allowed actions are: follow, unfollow"},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(id=user_id).first()

        if not user:
            return Response({"detail": f"User not found with id {user_id}."}, status=status.HTTP_400_BAD_REQUEST)

        fr = FollowRelation.objects.filter(from_user=request.user, to_user=user).first()
        if action == "follow":
            if not fr:
                FollowRelation.objects.create(from_user=request.user, to_user=user)
        else:
            if fr:
                fr.delete()
        return Response({"action": action, "user_id": user_id})
