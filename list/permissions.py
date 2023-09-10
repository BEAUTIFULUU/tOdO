from rest_framework import permissions


class ListOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class TaskOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.list.user == request.user
