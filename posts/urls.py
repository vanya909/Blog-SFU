from django.urls import path
from . import views

urlpatterns = [
    path('group/', views.study_group_posts, name='study_group_posts'),
]
