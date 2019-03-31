from rest_framework import serializers
from django.contrib.auth.models import User
from backend.models import *


class UserProfileSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = UserProfile
        fields = ('id', 'mobile', 'real_name', 'email')


class EventListSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    checkin_enabled = serializers.ReadOnlyField()
    host_display_info = serializers.ReadOnlyField()
    host_id = serializers.ReadOnlyField(source='host.id')

    class Meta:
        model = Event
        fields = ['id', 'title', 'host_id', 'host_display_info', 'checkin_enabled',
                  'start_time', 'end_time', 'location', 'require_approve']


class EventDetailSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    checkin_enabled = serializers.ReadOnlyField()
    host_display_info = serializers.ReadOnlyField()
    host_id = serializers.ReadOnlyField(source='host.id')

    class Meta:
        model = Event
        fields = ['id', 'title', 'host_id', 'host_display_info',
                  'description', 'checkin_enabled', 'start_time',
                  'end_time', 'location', 'public', 'require_approve']


class TransportSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    event = EventListSerializer(read_only=True)
    id = serializers.ReadOnlyField()

    class Meta:
        model = Transport
        fields = ['id', 'transport_type', 'transport_id', 'depart_station', 'depart_station',
                  'depart_time', 'arrival_station', 'arrival_time', 'other_detail',
                  'user', 'event']


class UserRegisterEventSerializer(serializers.ModelSerializer):
    user_info = UserProfileSerializer(source='user', read_only=True)
    transport_info = TransportSerializer(source='transport', read_only=True)
    event_info = EventListSerializer(source='event', read_only=True)
    date_registered = serializers.ReadOnlyField()
    checked_in = serializers.ReadOnlyField()

    class Meta:
        model = UserRegisterEvent
        fields = ['user_info', 'event_info', 'date_registered', 'transport_info', 'checked_in']


class UserManageEventSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    event = EventListSerializer(read_only=True)

    class Meta:
        model = UserManageEvent
        fields = ['user', 'event']


class CheckInSerializer(serializers.ModelSerializer):
    event = EventListSerializer()

    class Meta:
        model = CheckIn
        fields = ['token', 'event']

