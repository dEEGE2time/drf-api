from django.http import Http404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer
from drf_api.permissions import isOwnerOrReadOnly


class PostList(APIView):
    # Create Post form
    serializer_class = PostSerializer
    # Cannot create posts if not logged in
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    # List all posts
    def get(self, request):
        # Retrieve post instances from database
        posts = Post.objects.all()
        # Serialize them
        serializer = PostSerializer(
            posts, 
            many=True, 
            context={'request': request},
        )
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PostSerializer(
            data=request.data,
            context={'request': request},
        )
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
                )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class PostDetail(APIView):
    # Post form renders in browser
    serializer_class = PostSerializer
    # Cannot edit/delete posts if not logged in
    permission_classes = [isOwnerOrReadOnly]

    def get_object(self, pk):
        # Check post exist
        try:
            post = Post.objects.get(pk=pk)
            self.check_object_permissions(self.request, post)
            return post
        except Post.DoesNotExist:
            raise Http404

    # CREATE
    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(
            post,
            context={'request': request}
        )
        return Response(serializer.data)
    
    # EDIT
    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(
            post,
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )

    # DELETE
    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )