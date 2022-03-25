from django.urls import path
from .views import study_group_posts_view, post_detail_view

urlpatterns = [
    path('<int:pk>/', post_detail_view, name='post_detail'),
    path('group/', study_group_posts_view, name='study_group_posts'),
]
