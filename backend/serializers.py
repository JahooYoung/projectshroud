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
        fields = ['id', 'title', 'host_id', 'host_display_info', 'checkin_enabled',
                  'start_time', 'end_time', 'location', 'require_approve']


class EventDetailSerializer(serializers.ModelSerializer):
    host_display_info = serializers.ReadOnlyField()
    host_id = serializers.ReadOnlyField(source='host.id')

    class Meta:
        model = Event
        fields = ['id', 'title', 'host_id', 'host_display_info',
                  'description', 'checkin_enabled', 'start_time',
                  'end_time', 'location', 'public', 'require_approve']


class TransportSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    event = EventListSerializer()

    class Meta:
        model = Transport
        fields = '__all__'


class UserRegisterEventSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer(source='user')
    transport = TransportSerializer(source='registered_transport')
    event = EventListSerializer()

    class Meta:
        model = UserRegisterEvent
        fields = ['userprofile', 'event', 'date_registered', 'transport', 'checked_in']


class UserManageEventSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    event = EventListSerializer()

    class Meta:
        model = UserManageEvent
        fields = ['user', 'event']


class CheckInSerializer(serializers.ModelSerializer):
    event = EventListSerializer()

    class Meta:
        model = CheckIn
        fields = ['token', 'event']

