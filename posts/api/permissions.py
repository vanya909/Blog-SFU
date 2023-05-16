from rest_framework.permissions import BasePermission, SAFE_METHODS

from ..models import Post, Comment


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


class IsUserInGroup(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Post):
            if obj.only_for_group:
                return request.user.group == obj.author.group
        elif isinstance(obj, Comment):
            if obj.post.only_for_group:
                return request.user.group == obj.post.author.group
        return True
