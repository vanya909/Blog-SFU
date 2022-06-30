from rest_framework import viewsets, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from posts.models import Post
from users.models import StudyGroup, User, Follow
from .serializers import (PostSerializer, GroupSerializer,
                          UserSerializer, UserCreateSerializer,
                          PostCreateSerializer)
from .permissions import IsOwnerOrReadOnly


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(only_for_group=False)
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return PostCreateSerializer
        return PostSerializer


class GroupsViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    queryset = StudyGroup.objects.all()
    serializer_class = GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    @action(detail=False, permission_classes=(IsAuthenticated,))
    def me(self, request):
        user = request.user
        response = UserSerializer(user, context={'request': request})
        return Response(response.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        permission_classes=(IsAuthenticated,),
        methods=('post', 'delete')
    )
    def subscribe(self, request, pk):
        user = request.user
        author = get_object_or_404(User, pk=pk)
        if request.method == 'POST':
            Follow.objects.create(user=user, author=author)
            response = UserSerializer(author, context={'request': request})
            return Response(response.data, status=status.HTTP_200_OK)
        user.following.filter(author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
