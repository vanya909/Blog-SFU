from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ModelSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from ..serializers import UserCreateSerializer, UserRetrieveSerializer
from ...models import User


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    http_method_names = ('get', 'post')

    def get_serializer_class(self) -> type[ModelSerializer]:
        if self.action == "create":
            return UserCreateSerializer
        elif self.action in ("retrieve", "list"):
            return UserRetrieveSerializer

    def get_permissions(self) -> tuple[BasePermission]:
        if self.action == "me":
            return (IsAuthenticated(),)
        return (AllowAny(),)

    @action(
        methods=("get",),
        detail=False,
    )
    def me(self, request: Request) -> Response:
        return Response(UserRetrieveSerializer(request.user).data)
