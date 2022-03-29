from django.urls import path
from .views import study_group_posts_view, subscriptions_posts_view, post_detail_view, post_create_view, post_edit_view
from .views import comment_create_view

urlpatterns = [
    path('<int:pk>/', post_detail_view, name='post_detail'),
    path('<int:post_pk>/comment/', comment_create_view, name='comment_create'),
    path('group/', study_group_posts_view, name='study_group_posts'),
    path('subscriptions/', subscriptions_posts_view, name='subscriptions_posts'),
    path('create/', post_create_view, name='create_post'),
    path('<int:post_id>/edit/', post_edit_view, name='post_edit')
]
