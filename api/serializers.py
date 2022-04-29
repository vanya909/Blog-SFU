from rest_framework.serializers import ModelSerializer
from posts.models import Post


class PostSerializer(ModelSerializer):
    """Class which serializes posts"""
    class Meta:
        model = Post
        fields = '__all__'
