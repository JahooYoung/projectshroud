from rest_framework import permissions
from backend.models import *
from rest_framework.serializers import ValidationError


def is_site_admin(user):
    return user.is_staff


def is_activated_user(user):
    return bool(
            user
            and not isinstance(user, AnonymousUser)
            and user.is_activated
        )

class IsActivated(permissions.BasePermission):

    def has_permission(self, request, view):
        return is_activated_user(request.user)


class IsActivatedOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if is_activated_user(request.user):
            return True
        return False


class IsSiteAdminOrSelf(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if 'user_id' in self.request.data:
            try:
                theuser = get_user_model().objects.get(id=self.request.data.get('user_id'))
            except get_user_model().DoesNotExist:
                raise ValidationError('User Not Found.')
            if not is_site_admin(user) and user != theuser:
                return False

        return True


class IsSiteAdminOrEventManager(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if is_site_admin(user):
            return True

        data = request.data

        if 'event_id' not in data:
            raise ValidationError('No event_id specified.')
        try:
            event = Event.objects.get(id=data.get('event_id'))
        except Event.DoesNotExist:
            raise ValidationError('Event Not Found.')

        return UserManageEvent.objects.filter(user=user, event=event).exists()


class IsEventHostAdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read permissions: GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions.
        if not is_active_user(user):
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
        if not is_active_user(user):
            return False

        if isinstance(obj, Event):
            return (obj.host == request.user or
                    UserManageEvent.objects.filter(user=request.user, event=obj).exists())
        elif hasattr(obj, 'event'):
            return (obj.event.host == request.user or
                    UserManageEvent.objects.filter(user=request.user, event=obj.event).exists())
        return False


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read & Write permissions.
        if not is_active_user(user):
            return False
        if not hasattr(obj, 'user'):
            return False
        return obj.user == request.user


