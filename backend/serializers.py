from rest_framework import serializers
from django.contrib.auth.models import User
from backend.models import *


class UserProfileSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    is_activated = serializers.ReadOnlyField()

    class Meta:
        model = UserProfile
        fields = ('id', 'mobile', 'real_name', 'email', 'is_activated', 'receive_email')


class EventListSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    checkin_enabled = serializers.ReadOnlyField()
    host_display_info = serializers.ReadOnlyField()
    host_id = serializers.ReadOnlyField(source='host.id')
    attendee_count = serializers.ReadOnlyField()
    applicant_count = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = ['id', 'title', 'host_id', 'host_display_info', 'checkin_enabled',
                  'start_time', 'end_time', 'location', 'require_approve',
                  'attendee_count', 'applicant_count']


class EventDetailSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    checkin_enabled = serializers.ReadOnlyField()
    host_display_info = serializers.ReadOnlyField()
    host_id = serializers.ReadOnlyField(source='host.id')
    attendee_count = serializers.ReadOnlyField()
    applicant_count = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = ['id', 'title', 'host_id', 'host_display_info',
                  'description', 'description_html', 'checkin_enabled', 'start_time',
                  'end_time', 'location', 'public', 'require_approve',
                  'require_application', 'require_attachment',
                  'attendee_count', 'applicant_count']


class TransportSerializer(serializers.ModelSerializer):
    user_info = UserProfileSerializer(source='user', read_only=True)
    event_info = EventListSerializer(source='event', read_only=True)
    id = serializers.ReadOnlyField()

    class Meta:
        model = Transport
        fields = ['id', 'transport_type', 'transport_id', 'depart_station',
                  'depart_time', 'arrival_station', 'arrival_time', 'other_detail',
                  'user_info', 'event_info']


class UserRegisterEventSerializer(serializers.ModelSerializer):
    user_info = UserProfileSerializer(source='user', read_only=True)
    transport_info = TransportSerializer(source='transport', read_only=True)
    event_info = EventListSerializer(source='event', read_only=True)
    date_registered = serializers.ReadOnlyField()
    date_approved = serializers.ReadOnlyField()
    checked_in = serializers.ReadOnlyField()
    is_admin = serializers.ReadOnlyField()
    approved = serializers.ReadOnlyField()

    class Meta:
        model = UserRegisterEvent
        fields = ['user_info', 'event_info', 'date_registered', 'transport_info', 'checked_in',
                  'date_approved', 'application_text', 'approved', 'is_admin']


class UserManageEventSerializer(serializers.ModelSerializer):
    user_info = UserProfileSerializer(source='user', read_only=True)
    event_info = EventListSerializer(source='event', read_only=True)

    class Meta:
        model = UserManageEvent
        fields = ['user_info', 'event_info']


class CheckInSerializer(serializers.ModelSerializer):
    event_info = EventListSerializer(source='event', read_only=True)
    checkin_token = serializers.ReadOnlyField(source='token')
    started = serializers.ReadOnlyField()
    count = serializers.ReadOnlyField()

    class Meta:
        model = CheckIn
        fields = ['checkin_token', 'event_info', 'name', 'started', 'count']

