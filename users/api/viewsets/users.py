from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ModelSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from ..serializers import UserCreateSerializer, UserRetrieveSerializer
from ...models import User, Follow


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    http_method_names = ('get', 'post')

    def get_serializer_class(self) -> type[ModelSerializer]:
        if self.action == "create":
            return UserCreateSerializer
        elif self.action in ("retrieve", "list"):
            return UserRetrieveSerializer

    def get_permissions(self) -> tuple[BasePermission]:
        if self.action in ("me", "follow", "unfollow"):
            return (IsAuthenticated(),)
        return (AllowAny(),)

    @action(
        methods=("get",),
        detail=False,
    )
    def me(self, request: Request) -> Response:
        return Response(UserRetrieveSerializer(request.user).data)

    @action(
        methods=("get",),
        detail=True,
    )
    def follow(self, request: Request, pk=None) -> Response:
        author = self.get_object()
        if not Follow.objects.filter(
            user=request.user,
            author=author,
        ).exists():
            Follow.objects.create(
                user=request.user,
                author=author,
            )
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=("get",),
        detail=True,
    )
    def unfollow(self, request: Request, pk=None) -> Response:
        author = self.get_object()
        follow = Follow.objects.filter(
            user=request.user,
            author=author,
        ).first()
        if follow:
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
