from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework import permissions
from backend.models import Event
from backend.serializers import EventSerializer, UserProfileSerializer
from backend.permissions import IsOwnerOrReadOnly


class UserList(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserProfileSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserProfileSerializer


class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        # Todo
        serializer.save(host=self.request.user.userprofile)


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)


def index(request):
    return render(request, 'index.html', {})