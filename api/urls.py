from django.urls import path
from .views import get_public_posts


urlpatterns = [
    path('posts/', get_public_posts, name='get_public_posts'),
]
