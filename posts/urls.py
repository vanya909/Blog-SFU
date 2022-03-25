from django.urls import path
from .views import study_group_posts_view, post_detail_view, create_post, post_edit

urlpatterns = [
    path('<int:pk>/', post_detail_view, name='post_detail'),
    path('group/', study_group_posts_view, name='study_group_posts'),
    path('create/', create_post, name='create_post'),
    path('<int:post_id>/edit/', post_edit, name='post_edit')
]
