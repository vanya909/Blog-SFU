from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import Serializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models.query import QuerySet

from ...models import Post
from ..serializers import PostCreateSerializer, PostRetrieveSerializer, PostUpdateSerializer
from ..permissions import IsAuthorOrReadOnly, IsUserInGroup


class PostsViewSet(ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = (
        IsAuthorOrReadOnly,
        IsAuthenticatedOrReadOnly,
        IsUserInGroup,
    )

    def get_serializer_class(self) -> type[Serializer]:
        if self.action == "create":
            return PostCreateSerializer
        elif self.action in ("list", "retrieve"):
            return PostRetrieveSerializer
        elif self.action in ("update", "partial_update"):
            return PostUpdateSerializer

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(only_for_group=False)
