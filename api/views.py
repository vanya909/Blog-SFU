from rest_framework.response import Response
from rest_framework.decorators import api_view

from posts.models import Post
from .serializers import PostSerializer


@api_view(http_method_names=['GET'])
def get_public_posts(request):
    """API that returns all public posts"""
    posts = Post.objects.filter(only_for_group=False)
    serializer = PostSerializer(posts, many=True)

    return Response(serializer.data)
