from rest_framework.serializers import ModelSerializer

from ...models import Tag


class TagRetrieveSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "title")
