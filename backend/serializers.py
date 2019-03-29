from rest_framework import serializers
from django.contrib.auth.models import User
from backend.models import *


class UserProfileSerializer(serializers.ModelSerializer):
    userregisterevent = serializers.RelatedField(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'mobile', 'real_name', 'email', 'userregisterevent')


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
    class Meta:
        model = Transport
        fields = '__all__'


class UserRegisterEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRegisterEvent
        fields = '__all__'


class UserManageEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserManageEvent
        fields = '__all__'
