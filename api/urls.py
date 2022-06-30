from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PostsViewSet, GroupsViewSet, UserViewSet

router = DefaultRouter()

router.register(
    'users',
    UserViewSet,
    basename='users'
)

router.register(
    'posts',
    PostsViewSet,
    basename='posts'
)

router.register(
    'groups',
    GroupsViewSet,
    basename='groups'
)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
