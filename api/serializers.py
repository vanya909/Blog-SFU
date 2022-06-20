from rest_framework.serializers import ModelSerializer
from posts.models import Post
from users.models import User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'second_name', 'group')


class PostSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'description', 'pub_date', 'update_date', 'author')
