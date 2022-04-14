from django.urls import path
from .views import (post_detail_view, subscriptions_posts_view, study_group_posts_view,
                    post_create_view, post_edit_view, post_delete_view,
                    comment_create_view, comment_delete_view)

urlpatterns = [
    path('<int:pk>/', post_detail_view, name='post_detail'),
    path('<int:post_pk>/comment/', comment_create_view, name='comment_create'),
    path('<int:post_pk>/comment/<int:comment_pk>/delete/', comment_delete_view, name='comment_delete'),
    path('group/', study_group_posts_view, name='study_group_posts'),
    path('subscriptions/', subscriptions_posts_view, name='subscriptions_posts'),
    path('create/', post_create_view, name='create_post'),
    path('<int:post_pk>/edit/', post_edit_view, name='post_edit'),
    path('<int:post_pk>/delete/', post_delete_view, name='post_delete'),
]
