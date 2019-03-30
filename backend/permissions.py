from rest_framework import permissions
from backend.models import *


class IsEventHostAdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read permissions: GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions.
        if not request.user:
            return False

        if isinstance(obj, Event):
            return (obj.host == request.user or
                    UserManageEvent.objects.filter(user=request.user, event=obj).exists())
        elif hasattr(obj, 'event'):
            return (obj.event.host == request.user or
                    UserManageEvent.objects.filter(user=request.user, event=obj.event).exists())


class IsEventHostAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read & Write permissions.
        if not request.user:
            return False

        if isinstance(obj, Event):
            return (obj.host == request.user or
                    UserManageEvent.objects.filter(user=request.user, event=obj).exists())
        elif hasattr(obj, 'event'):
            return (obj.event.host == request.user or
                    UserManageEvent.objects.filter(user=request.user, event=obj.event).exists())
        return False


class IsEventRegistered(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read & Write permissions.
        if not request.user:
            return False

        if isinstance(obj, Event):
            return (obj.host == request.user or
                    UserRegisterEvent.objects.filter(user=request.user, event=obj).exists())
        elif hasattr(obj, 'event'):
            return (obj.event.host == request.user or
                    UserRegisterEvent.objects.filter(user=request.user, event=obj.event).exists())
        return False


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read & Write permissions.
        if not request.user:
            return False
        if not hasattr(obj, 'user'):
            return False
        return obj.user == request.user


# Whether an event is open for registration
class OpenRegistration(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read & Write permissions.
        if not request.user:
            return False
        if obj.event.require_approve:
            return False
        return obj.user == request.user

