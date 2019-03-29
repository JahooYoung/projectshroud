from rest_framework import serializers
from django.contrib.auth.models import User
from backend.models import *


class UserSerializer(serializers.ModelSerializer):
    events = serializers.PrimaryKeyRelatedField(many=True, queryset=Event.objects.all())

    class Meta:
        model = UserProfile
        fields = ('user.username', 'mobile', 'real_name', 'events')


class EventSerializer(serializers.ModelSerializer):
    host = serializers.ReadOnlyField(source='host.user')

    class Meta:
        model = Event
        fields = ('id', 'title', 'host', 'description', 'start_time', 'end_time',
                  'public', 'require_approve')


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
