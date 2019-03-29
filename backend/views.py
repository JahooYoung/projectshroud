from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from backend.models import Event
from backend.serializers import *
from backend.permissions import *
from django.utils import timezone
from django.http import Http404


# Todos: check-in(start/stop/checkin), QRcode, "cascade create"


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
    permission_classes = (IsOwner, )

    def get_queryset(self):
        # user = get_user_model().objects.get(id=self.kwargs.get('pk'))
        user = self.request.user
        return UserRegisterEvent.objects.filter(user=user)


class UserRegisterFutureEventList(generics.ListAPIView):
    serializer_class = UserRegisterEventSerializer
    permission_classes = (IsOwner, )

    def get_queryset(self):
        # user = get_user_model().objects.get(id=self.kwargs.get('pk'))
        user = self.request.user
        return UserRegisterEvent.objects.filter(user=user, start_time__gt=timezone.now())


class UserRegisterPastEventList(generics.ListAPIView):
    serializer_class = UserRegisterEventSerializer
    permission_classes = (IsOwner, )

    def get_queryset(self):
        # user = get_user_model().objects.get(id=self.kwargs.get('pk'))
        user = self.request.user
        return UserRegisterEvent.objects.filter(user=user, end_time__lte=timezone.now())


class UserRegisterOngoingEventList(generics.ListAPIView):
    serializer_class = UserRegisterEventSerializer
    permission_classes = (IsOwner, )

    def get_queryset(self):
        # user = get_user_model().objects.get(id=self.kwargs.get('pk'))
        user = self.request.user
        return UserRegisterEvent.objects.filter(user=user, start_time__lte=timezone.now(), end_time__gt=timezone.now())


class UserEventRegister(generics.CreateAPIView):
    # Not Tested

    serializer_class = UserRegisterEventSerializer
    permission_classes = (OpenRegistration|IsEventHostAdmin, )

    def perform_create(self, serializer):
        user = self.request.user
        data = self.request.data
        if 'user_id' in data:
            user = get_user_model().objects.get(id=data['user_id'])
        event = Event.objects.get(id=data.get('event_id'))
        transport = Transport.objects.get(id=data.get('transport_id'))
        serializer.save(user=user, event=event, transport=transport)


class AssignEventAdmin(generics.CreateAPIView):
    # Not Tested

    serializer_class = UserManageEventSerializer
    permission_classes = (IsEventHostAdmin, )

    def perform_create(self, serializer):
        data = self.request.data
        user = get_user_model().objects.get(id=data.get('user_id'))
        event = Event.objects.get(id=data.get('event_id'))
        serializer.save(user=user, event=event)


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    # Need More Test

    queryset = Event.objects.all()
    serializer_class = EventDetailSerializer
    permission_classes = (IsEventHostAdminOrReadOnly,)

    def get(self, request, *args, **kwargs):
        data = self.retrieve(request, *args, **kwargs).data
        try:
            obj = Event.objects.get(pk=kwargs.get('pk'))
        except Event.DoesNotExist:
            raise Http404

        data['event_admin'] = check_is_admin(request.user, obj)
        data['event_registered'] = check_event_registered(request.user, obj)
        return Response(data)


class EventAttendeeList(generics.ListAPIView):
    # Not Tested

    serializer_class = UserRegisterEventSerializer
    permission_classes = (IsEventRegistered|IsEventHostAdmin, )

    def get_queryset(self):
        try:
            event = Event.objects.get(pk=kwargs.get('pk'))
        except Event.DoesNotExist:
            raise Http404
        return UserRegisterEvent.objects.filter(event=event)


class TransportCreateView(generics.CreateAPIView):
    # Not Tested

    queryset = Transport.objects.all()
    serializer_class = TransportSerializer
    permission_classes = (IsOwner|IsEventHostAdmin,)

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
    permission_classes = (IsOwner|IsEventHostAdmin,)


def index(request):
    return render(request, 'index.html', {})