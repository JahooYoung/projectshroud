from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from backend.models import Event
from backend.serializers import *
from backend.permissions import *
from django.utils import timezone
from django.http import Http404


# Todos: QRcode, "cascade create"


def check_is_admin(user, event):
    return UserManageEvent.objects.filter(user=user, event=event).exists()


def check_event_registered(user, event):
    return UserRegisterEvent.objects.filter(user=user, event=event).exists()


class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.filter(public=True)
    serializer_class = EventListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        # user = get_user_model().objects.get(id=self.request.data.get('host_id', ''))
        user = self.request.user
        serializer.save(host=user)


class PastEventList(generics.ListAPIView):
    queryset = Event.objects.filter(public=True, end_time__lte=timezone.now())
    serializer_class = EventListSerializer


class FutureEventList(generics.ListAPIView):
    queryset = Event.objects.filter(public=True, start_time__gt=timezone.now())
    serializer_class = EventListSerializer


class OngoingEventList(generics.ListAPIView):
    queryset = Event.objects.filter(public=True, start_time__lte=timezone.now(), end_time__gt=timezone.now())
    serializer_class = EventListSerializer


class UserRegisterEventList(generics.ListAPIView):
    serializer_class = UserRegisterEventSerializer
    permission_classes = (permissions.IsAdminUser|IsOwner, )

    def get_queryset(self):
        # user = get_user_model().objects.get(id=self.kwargs.get('pk'))
        user = self.request.user
        return UserRegisterEvent.objects.filter(user=user)


class UserManageEventList(generics.ListAPIView):
    serializer_class = UserManageEventSerializer
    permission_classes = (permissions.IsAdminUser|IsOwner, )

    def get_queryset(self):
        # user = get_user_model().objects.get(id=self.kwargs.get('pk'))
        user = self.request.user
        return UserManageEvent.objects.filter(user=user)


class UserRegisterFutureEventList(generics.ListAPIView):
    serializer_class = UserRegisterEventSerializer
    permission_classes = (permissions.IsAdminUser|IsOwner, )

    def get_queryset(self):
        # user = get_user_model().objects.get(id=self.kwargs.get('pk'))
        user = self.request.user
        return UserRegisterEvent.objects.filter(user=user, start_time__gt=timezone.now())


class UserRegisterPastEventList(generics.ListAPIView):
    serializer_class = UserRegisterEventSerializer
    permission_classes = (permissions.IsAdminUser|IsOwner, )

    def get_queryset(self):
        # user = get_user_model().objects.get(id=self.kwargs.get('pk'))
        user = self.request.user
        return UserRegisterEvent.objects.filter(user=user, end_time__lte=timezone.now())


class UserRegisterOngoingEventList(generics.ListAPIView):
    serializer_class = UserRegisterEventSerializer
    permission_classes = (permissions.IsAdminUser|IsOwner, )

    def get_queryset(self):
        # user = get_user_model().objects.get(id=self.kwargs.get('pk'))
        user = self.request.user
        return UserRegisterEvent.objects.filter(user=user, start_time__lte=timezone.now(), end_time__gt=timezone.now())


class UserEventRegister(generics.CreateAPIView):
    # Not Tested

    serializer_class = UserRegisterEventSerializer
    permission_classes = (OpenRegistration|IsEventHostAdmin|permissions.IsAdminUser, )

    def perform_create(self, serializer):
        user = self.request.user
        data = self.request.data
        if 'user_id' in data:
            user = get_user_model().objects.get(id=data['user_id'])
        if 'event_id' not in data:
            raise Http404 # return Response(status=status.HTTP_400_BAD_REQUEST, data={'msg': 'No event_id specified.'})
        event = Event.objects.get(id=data.get('event_id'))
        if 'transport_id' not in data or data.get('transport_id') is None:
            transport = None
        else:
            transport = Transport.objects.get(id=data.get('transport_id'))
        serializer.save(user=user, event=event, transport=transport)


class AssignEventAdmin(generics.CreateAPIView):
    # Not Tested

    serializer_class = UserManageEventSerializer
    permission_classes = (IsEventHostAdmin|permissions.IsAdminUser, )

    def perform_create(self, serializer):
        data = self.request.data
        user = get_user_model().objects.get(id=data.get('user_id'))
        event = Event.objects.get(id=data.get('event_id'))
        serializer.save(user=user, event=event)


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    # Need More Test

    queryset = Event.objects.all()
    serializer_class = EventDetailSerializer
    permission_classes = (IsEventHostAdminOrReadOnly|permissions.IsAdminUser,)

    def get(self, request, *args, **kwargs):
        try:
            obj = Event.objects.get(pk=kwargs.get('pk'))
        except Event.DoesNotExist:
            raise Http404
        data = self.retrieve(request, *args, **kwargs).data

        data['event_admin'] = check_is_admin(request.user, obj)
        data['event_registered'] = check_event_registered(request.user, obj)
        return Response(data)


class EventAttendeeList(generics.ListAPIView):
    serializer_class = UserRegisterEventSerializer
    permission_classes = (IsEventRegistered|IsEventHostAdmin|permissions.IsAdminUser, )

    def get_queryset(self):
        try:
            event = Event.objects.get(pk=self.kwargs.get('pk'))
        except Event.DoesNotExist:
            return None
        return UserRegisterEvent.objects.filter(event=event)


class EventAdminList(generics.ListAPIView):
    serializer_class = UserManageEventSerializer
    permission_classes = (IsEventHostAdmin|permissions.IsAdminUser, )

    def get_queryset(self):
        try:
            event = Event.objects.get(pk=self.kwargs.get('pk'))
        except Event.DoesNotExist:
            return None
        return UserManageEvent.objects.filter(event=event)


class TransportCreateView(generics.CreateAPIView):
    # Not Tested

    queryset = Transport.objects.all()
    serializer_class = TransportSerializer
    permission_classes = (IsOwner|IsEventHostAdmin|permissions.IsAdminUser,)

    def perform_create(self, serializer):
        user = self.request.user
        data = self.request.data
        if 'user_id' in data:
            user = get_user_model().objects.get(id=data['user_id'])
        event = Event.objects.get(id=data.get('event_id'))
        serializer.save(user=user, event=event)


class TransportView(generics.RetrieveUpdateDestroyAPIView):
    # Not Tested

    queryset = Transport.objects.all()
    serializer_class = TransportSerializer
    permission_classes = (IsOwner|IsEventHostAdmin|permissions.IsAdminUser,)


class EventCheckInToken(APIView):
    def get(self, request, pk, format=None):
        try:
            eventobj = CheckIn.objects.get(pk=pk)
        except CheckIn.DoesNotExist:
            raise Http404

        if not event.checkin_enabled:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'msg': 'Event Check-in not enabled.'})
        data = {'checkin_token': CheckIn.objects.get(event=event).token}
        return Response(status=status.HTTP_200_OK, data=data)

    def post(self, request, pk, format=None):
       return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class UserCheckInEvent(APIView):
    # Not Tested

    permission_classes = (IsOwner|IsEventHostAdmin|permissions.IsAdminUser,)

    def get(self, request, pk, format=None):
        try:
            checkinobj = CheckIn.objects.get(pk=pk)
        except CheckIn.DoesNotExist:
            raise Http404

        event = checkinobj.event
        if not event.checkin_enabled:
            # Should not reach here
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'msg': 'Event Check-in not enabled.'})
        user = request.user
        if 'user_id' in request.data:
            user = get_user_model().objects.get(id=request.data.get('user_id'))

        try:
            ure_obj = UserRegisterEvent.objects.get(user=user, event=event)
        except UserRegisterEvent.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'msg': 'Not registered.'})

        if ure_obj.checked_in:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'msg': 'Already checked in.'})
        ure_obj.checkin()
        ure_obj.save()
        return Response(status=status.HTTP_200_OK)

    def post(self, request, pk, format=None):
        return self.get(request, pk, format)


class StartCheckIn(generics.CreateAPIView):
    # Not Tested

    queryset = CheckIn.objects.all()
    serializer_class = CheckInSerializer
    permission_classes = (IsEventHostAdmin|permissions.IsAdminUser,)

    def perform_create(self, serializer):
        data = self.request.data
        event = Event.objects.get(id=data.get('event_id'))
        if event.checkin_enabled:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'msg': 'Check-in already started.'})
        event.enable_checkin()
        event.save()
        serializer.save(event=event)


class StopCheckIn(generics.DestroyAPIView):
    # Not Tested

    queryset = CheckIn.objects.all()
    serializer_class = CheckInSerializer
    permission_classes = (IsEventHostAdmin|permissions.IsAdminUser,)

    def perform_destroy(self, instance):
        if instance is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'msg': 'Check-in not started.'})
        event = instance.event
        event.disable_checkin()
        instance.delete()


def index(request):
    return render(request, 'index.html', {})

