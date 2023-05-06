from django.urls import path, include


urlpatterns = [
    path('auth/', include('users.api.urls.auth')),
    path('users/', include('users.api.urls.users')),
]
