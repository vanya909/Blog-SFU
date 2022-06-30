from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from posts.models import Post
from users.models import User, StudyGroup


class GroupSerializer(ModelSerializer):

    class Meta:
        model = StudyGroup
        fields = '__all__'


class UserSerializer(ModelSerializer):
    group = GroupSerializer(read_only=True)
    is_me_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'second_name', 'group', 'is_me_subscribed')

    def get_is_me_subscribed(self, obj):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        return user.following.filter(author=obj).exists()


class PostSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)
    is_me_liked_post = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'description', 'pub_date', 'update_date', 'author', 'only_for_group', 'is_me_liked_post')

    def get_is_me_liked_post(self, obj):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        return user.likes.filter(post=obj).exists()


class UserCreateSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'second_name', 'email', 'password', 'group')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user


class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('description', 'only_for_group')

    def create(self, validated_data):
        author = self.context.get('request').user
        post = Post.objects.create(**validated_data, author=author)
        return post
