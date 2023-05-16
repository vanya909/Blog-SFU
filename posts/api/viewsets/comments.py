from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ...models import Comment
from ..serializers import CommentRetrieveSerializer, CommentCreateSerializer
from ..permissions import IsUserInGroup


class CommentsViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = (IsUserInGroup, IsAuthenticatedOrReadOnly)

    def get_serializer_class(self):
        if self.action == "create":
            return CommentCreateSerializer
        return CommentRetrieveSerializer
