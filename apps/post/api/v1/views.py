from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination

from apps.post.models import Post
from apps.post.api.v1.serializers import PostSerializer


class PostView(generics.ListAPIView, generics.CreateAPIView):
    queryset = Post.objects.active()
    permission_classes = (AllowAny,)
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination
