from typing import OrderedDict

from rest_framework import serializers

from ...models import Post, Tag
from users.api.serializers import UserRetrieveSerializer
from ..serializers import TagRetrieveSerializer


class PostRetrieveSerializer(serializers.ModelSerializer):
    author = UserRetrieveSerializer(read_only=True)
    tags = TagRetrieveSerializer(many=True, read_only=True)
    likes = serializers.SerializerMethodField(
        method_name="get_likes_count",
    )

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "only_for_group",
            "description",
            "tags",
            "pub_date",
            "update_date",
            "likes",
        )

    def get_likes_count(self, obj: Post) -> int:
        return obj.likes.count()


class PostCreateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        allow_null=True,
    )

    class Meta:
        model = Post
        fields = ("only_for_group", "description", "tags")

    def create(self, validated_data: dict) -> Post:
        author = self.context.get("request").user
        tags = validated_data.pop("tags")
        post = Post.objects.create(**validated_data, author=author)
        if tags:
            for tag in tags:
                post.tags.add(tag)
        post.save()
        return post

    @property
    def data(self) -> OrderedDict:
        return PostRetrieveSerializer(instance=self.instance).data


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "only_for_group", "description", "tags")
        read_only_fields = ("id",)

    def update(self, instance: Post, validated_data: dict) -> Post:
        instance.only_for_group = validated_data.get('only_for_group', instance.only_for_group)
        instance.description = validated_data.get('description', instance.description)
        if instance.tags != validated_data.get("tags"):
            instance.tags.clear()
            for tag in validated_data.get("tags"):
                instance.tags.add(tag)
        instance.save()
        return instance

    @property
    def data(self) -> OrderedDict:
        return PostRetrieveSerializer(instance=self.instance).data
