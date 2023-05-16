from typing import OrderedDict

from rest_framework import serializers

from ...models import Comment, Post
from users.api.serializers import UserRetrieveSerializer
from ..constants import comments as comments_constants


class CommentRetrieveSerializer(serializers.ModelSerializer):
    author = UserRetrieveSerializer()

    class Meta:
        model = Comment
        fields = ("id", "post", "author", "text", "pub_date")


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("post", "text")

    def validate_post(self, value: Post):
        user = self.context.get("request").user
        if not Post.objects.filter(pk=value.pk, author__group=user.group).exists():
            raise serializers.ValidationError(comments_constants.YOU_ARE_NOT_IN_THIS_GROUP)
        return value

    def create(self, validated_data: dict) -> Comment:
        author = self.context.get("request").user
        validated_data.update({"author": author})
        return super().create(validated_data)

    @property
    def data(self) -> OrderedDict:
        return CommentRetrieveSerializer(instance=self.instance).data
