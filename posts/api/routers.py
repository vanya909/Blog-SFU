from rest_framework.routers import DefaultRouter

from .viewsets import PostsViewSet, CommentsViewSet


posts_router = DefaultRouter()
posts_router.register("", PostsViewSet)

comments_router = DefaultRouter()
comments_router.register("", CommentsViewSet)
