from django.urls import path
from .views import signup_view, profile_view


urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('<username>', profile_view, name='profile')
]
