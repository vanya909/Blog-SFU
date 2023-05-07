from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ...models import User
from ..serializers import UserRetrieveSerializer


class UserSummaryAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserRetrieveSerializer

    def get_object(self) -> User:
        return self.request.user
