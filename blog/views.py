from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Post
from .serializers import PostReadSerializer, PostCreateSerializer, PostUpdateSerializer, VoteModeEnums, \
    PostVoteSerializer


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostReadSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return PostCreateSerializer
        elif self.action == "update":
            return PostUpdateSerializer
        elif self.action == "vote":
            return PostVoteSerializer
        return PostReadSerializer

    @action(detail=True, methods=["PUT"])
    def vote(self, request, pk=None):
        post: Post = self.get_object()
        serializer = PostVoteSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data["mode"] == VoteModeEnums.UPVOTE:
                post.upvotes.add(request.user)
                if request.user in post.downvotes.all():
                    post.downvotes.remove(request.user)
            else:
                post.downvotes.add(request.user)
                if request.user in post.upvotes.all():
                    post.upvotes.remove(request.user)
            return Response({"upvote_count": post.upvote_count, "downvote_count": post.downvote_count,
                             "is_upvoted": request.user in post.upvotes.all(),
                             "is_downvoted": request.user in post.downvotes.all()})
        return Response({"detail": "Payload is wrong."}, status=status.HTTP_400_BAD_REQUEST)
