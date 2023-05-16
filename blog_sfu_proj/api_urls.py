from django.urls import path, include

from posts.api.routers import posts_router, comments_router


urlpatterns = [
    path("auth/", include("users.api.urls.auth")),
    path("users/", include("users.api.urls.users")),
    path("posts/", include(posts_router.urls)),
    path("comments/", include(comments_router.urls)),
]
