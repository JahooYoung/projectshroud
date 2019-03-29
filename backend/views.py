from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from backend.models import Event
from backend.serializers import *
from backend.permissions import IsOwnerOrReadOnly
from django.utils import timezone


class UserList(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserProfileSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserProfileSerializer


class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.all().filter(public=True)
    serializer_class = EventListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        # user = get_user_model().objects.get(id=self.request.data.get('host_id', ''))
        user = self.request.user
        serializer.save(host=user)


class PastEventList(generics.ListAPIView):
    queryset = Event.objects.all().filter(public=True, end_time__lte=timezone.now())
    serializer_class = EventListSerializer


class FutureEventList(generics.ListAPIView):
    queryset = Event.objects.all().filter(public=True, start_time__gte=timezone.now())
    serializer_class = EventListSerializer


class OngoingEventList(generics.ListAPIView):
    queryset = Event.objects.all().filter(public=True, start_time__lte=timezone.now(), end_time__gt=timezone.now())
    serializer_class = EventListSerializer


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventDetailSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)


def index(request):
    return render(request, 'index.html', {})