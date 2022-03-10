from django.contrib import admin
from .models import User, StudyGroup, Follow


admin.site.register(User)
admin.site.register(StudyGroup)
admin.site.register(Follow)
