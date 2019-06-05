from rest_framework import permissions
from backend.models import *
from rest_framework.serializers import ValidationError
from django.http import Http404


def is_site_admin(user):
    if isinstance(user, AnonymousUser):
        return False
    return user.is_staff


def is_activated_user(user):
    return bool(
            user
            and not isinstance(user, AnonymousUser)
            and user.is_activated
        )


class IsAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user and request.user.is_staff)

    def has_object_permission(self, request, view, object):
        return self.has_permission(request, view)


class IsActivated(permissions.BasePermission):

    def has_permission(self, request, view):
        return is_activated_user(request.user)

    def has_object_permission(self, request, view, object):
        return self.has_permission(request, view)


class IsActivatedOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if is_activated_user(request.user):
            return True
        return False

    def has_object_permission(self, request, view, object):
        return self.has_permission(request, view)


class IsSiteAdminOrSelf(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if 'user_id' in request.data:
            try:
                theuser = get_user_model().objects.get(id=request.data.get('user_id'))
            except get_user_model().DoesNotExist:
                raise ValidationError('User Not Found.')
            if not is_site_admin(user) and user != theuser:
                return False

        return True

    def has_object_permission(self, request, view, object):
        return self.has_permission(request, view)


class IsSiteAdminOrEventManager(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        pk = view.kwargs.get('pk')

        if pk is not None:
            if view.pk_type == 'event':
                try:
                    event = Event.objects.get(pk=pk)
                except Event.DoesNotExist:
                    raise Http404
                return UserManageEvent.objects.filter(user=user, event=event).exists()
            if view.pk_type == 'checkin':
                try:
                    event = CheckIn.objects.get(pk=pk).event
                except CheckIn.DoesNotExist:
                    raise Http404
                return UserManageEvent.objects.filter(user=user, event=event).exists()

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

    def has_object_permission(self, request, view, object):
        return self.has_permission(request, view)


class IsEventHostAdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read permissions: GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions.
        if not is_activated_user(request.user):
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
        if not is_activated_user(request.user):
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
        if not is_activated_user(request.user):
            return False
        if not hasattr(obj, 'user'):
            return False
        return obj.user == request.user


