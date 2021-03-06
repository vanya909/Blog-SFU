from django.urls import path
from .views import (post_detail_view, subscriptions_posts_view, study_group_posts_view,
                    post_create_view, post_edit_view, post_delete_view,
                    comment_create_view, comment_edit_view, comment_delete_view,
                    like_view, subscriptions_user_posts_view)

urlpatterns = [
    path('<int:post_pk>/', post_detail_view, name='post_detail'),
    path('<int:post_pk>/comment/', comment_create_view, name='comment_create'),
    path('<int:post_pk>/comment/<int:comment_pk>/edit/', comment_edit_view, name='comment_edit'),
    path('<int:post_pk>/comment/<int:comment_pk>/delete/', comment_delete_view, name='comment_delete'),
    path('group/', study_group_posts_view, name='study_group_posts'),
    path('subscriptions/', subscriptions_posts_view, name='subscriptions_posts'),
    path('subscriptions/<str:username>', subscriptions_user_posts_view, name='subscriptions_user_posts'),
    path('create/', post_create_view, name='create_post'),
    path('<int:post_pk>/edit/', post_edit_view, name='post_edit'),
    path('<int:post_pk>/delete/', post_delete_view, name='post_delete'),
    path('<int:post_pk>/like/', like_view, name='like'),
]
