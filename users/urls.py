from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('<str:username>', views.profile_view, name='profile'),
    path('<str:username/follow>', views.profile_follow, name='profile_follow'),
    path('<str:username/unfollow>', views.profile_unfollow, name='profile_unfollow'),
]
