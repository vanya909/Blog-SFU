from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('posts/', include('posts.urls')),
    path('api/', include('blog_sfu_proj.api_urls')),
    path('', include('pages.urls')),
]

handler404 = "posts.views.page_not_found"
handler500 = "posts.views.server_error"
