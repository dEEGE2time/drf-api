from rest_framework import generics, permissions
from .models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer
from drf_api.permissions import isOwnerOrReadOnly


class CommentList(generics.ListCreateAPIView):
        serializer_class = CommentSerializer
        permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        # We want all comments, comments are not insensitive data, google "data filtering drf"
        queryset = Comment.objects.all()

        def perform_create(self, serializer):
            serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    #Only comment owner can edit/delete comment
    permission_classes = [isOwnerOrReadOnly]
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()

