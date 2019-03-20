from rest_framework import serializers
from django.contrib.auth.models import User
from backend.models import Event


class UserSerializer(serializers.ModelSerializer):
    events = serializers.PrimaryKeyRelatedField(many=True, queryset=Event.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'events')


class EventSerializer(serializers.ModelSerializer):
    host = serializers.ReadOnlyField(source='host.username')

    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'start_time', 'host')