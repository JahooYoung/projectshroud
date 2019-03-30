from rest_framework import serializers
from django.contrib.auth.models import User
from backend.models import *


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'mobile', 'real_name', 'email')


class EventListSerializer(serializers.ModelSerializer):
    host_display_info = serializers.ReadOnlyField()
    host_id = serializers.ReadOnlyField(source='host.id')

    class Meta:
        model = Event
        fields = ['id', 'title', 'host_id', 'host_display_info',
                  'start_time', 'end_time', 'location', 'require_approve']


class EventDetailSerializer(serializers.ModelSerializer):
    host_display_info = serializers.ReadOnlyField()
    host_id = serializers.ReadOnlyField(source='host.id')

    class Meta:
        model = Event
        fields = ['id', 'title', 'host_id', 'host_display_info', 'description',
                  'start_time', 'end_time', 'location', 'public', 'require_approve']


class TransportSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    event = EventListSerializer(read_only=True)
    class Meta:
        model = Transport
        fields = '__all__'


class UserRegisterEventSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer(source='user', read_only=True)
    transport = TransportSerializer(source='registered_transport', read_only=True)
    event = EventListSerializer(read_only=True)

    class Meta:
        model = UserRegisterEvent
        fields = ['userprofile', 'event', 'date_registered', 'transport', 'checked_in']


class UserManageEventSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    event = EventListSerializer(read_only=True)

    class Meta:
        model = UserManageEvent
        fields = ['user', 'event']
