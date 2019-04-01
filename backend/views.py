from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from backend.serializers import *
from backend.permissions import *
from django.utils import timezone
from django.http import Http404, HttpResponse
from rest_framework.serializers import ValidationError
from MyQR import myqr
import os


def check_is_admin(user, event):
    if user.id == event.host.id:
        return True
    return UserManageEvent.objects.filter(user=user, event=event).exists()


def check_event_registered(user, event):
    return UserRegisterEvent.objects.filter(user=user, event=event).exists()


@api_view(['GET', 'POST'])
def gen_qrcode(request):
    if 'text' not in request.data:
        raise serializers.ValidationError('No text provided.')

    filetoken = '%s.png' % generate_event_uuid()

    version, level, qr_name = myqr.run(
        request.data.get('text'),
        version=5,
        level='H',
        picture=None,
        colorized=False,
        contrast=1.0,
        brightness=1.0,
        save_name=filetoken,
        save_dir=os.path.join(os.getcwd(), 'qr_temp')
    )

    with open(qr_name, 'rb') as f:
        qr_img = f.read()
    os.remove(qr_name)

    return HttpResponse(qr_img, content_type='image/png')


class DummyView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        content = {
            'status': 'request was permitted'
        }
        return Response(content)


class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.filter(public=True)
    serializer_class = EventListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        # user = get_user_model().objects.get(id=self.request.data.get('host_id', ''))
        user = self.request.user
        desc = ''

        if 'description' in self.request.data:
            desc = self.request.data.get('description')

        serializer.save(host=user, description=desc)


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
    permission_classes = (permissions.IsAdminUser|IsOwner, )

    def get_queryset(self):
        # user = get_user_model().objects.get(id=self.kwargs.get('pk'))
        user = self.request.user
        return UserRegisterEvent.objects.filter(user=user)


class UserManageEventList(generics.ListAPIView):
    serializer_class = UserManageEventSerializer
    permission_classes = (permissions.IsAdminUser|IsOwner, )

    def get_queryset(self):
        # user = get_user_model().objects.get(id=self.kwargs.get('pk'))
        user = self.request.user
        return UserManageEvent.objects.filter(user=user)


class UserRegisterFutureEventList(generics.ListAPIView):
    serializer_class = UserRegisterEventSerializer
    permission_classes = (permissions.IsAdminUser|IsOwner, )

    def get_queryset(self):
        # user = get_user_model().objects.get(id=self.kwargs.get('pk'))
        user = self.request.user
        return UserRegisterEvent.objects.filter(user=user, start_time__gt=timezone.now())


class UserRegisterPastEventList(generics.ListAPIView):
    serializer_class = UserRegisterEventSerializer
    permission_classes = (permissions.IsAdminUser|IsOwner, )

    def get_queryset(self):
        # user = get_user_model().objects.get(id=self.kwargs.get('pk'))
        user = self.request.user
        return UserRegisterEvent.objects.filter(user=user, end_time__lte=timezone.now())


class UserRegisterOngoingEventList(generics.ListAPIView):
    serializer_class = UserRegisterEventSerializer
    permission_classes = (permissions.IsAdminUser|IsOwner, )

    def get_queryset(self):
        # user = get_user_model().objects.get(id=self.kwargs.get('pk'))
        user = self.request.user
        return UserRegisterEvent.objects.filter(user=user, start_time__lte=timezone.now(), end_time__gt=timezone.now())


class UserEventRegister(generics.CreateAPIView):
    serializer_class = UserRegisterEventSerializer
    permission_classes = (OpenRegistration|IsEventHostAdmin|permissions.IsAdminUser, )

    def perform_create(self, serializer):
        user = self.request.user
        data = self.request.data
        if 'user_id' in data:
            try:
                user = get_user_model().objects.get(id=data.get('user_id'))
            except Event.DoesNotExist:
                raise ValidationError('User Not Found.')

        if 'event_id' not in data:
            raise ValidationError('No event_id specified.')

        try:
            event = Event.objects.get(id=data.get('event_id'))
        except Event.DoesNotExist:
            raise ValidationError('Event Not found.')

        if check_event_registered(user, event):
            raise ValidationError('Already Registered.')

        transport = None
        if 'transport_id' in data:
            try:
                transport = Transport.objects.get(id=data.get('transport_id'))
            except Event.DoesNotExist:
                raise ValidationError('Transport Not found.')

        serializer.save(user=user, event=event, transport=transport)


class AssignEventAdmin(generics.CreateAPIView):
    # Not Tested

    serializer_class = UserManageEventSerializer
    permission_classes = (IsEventHostAdmin|permissions.IsAdminUser, )

    def perform_create(self, serializer):
        data = self.request.data
        try:
            user = get_user_model().objects.get(id=data.get('event_id'))
        except Event.DoesNotExist:
            raise ValidationError('User Not Found.')

        try:
            event = Event.objects.get(id=data.get('event_id'))
        except Event.DoesNotExist:
            raise ValidationError('Event Not found.')

        if check_is_admin(user, event):
            raise ValidationError('Is admin already.')

        serializer.save(user=user, event=event)


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    # Need More Test

    queryset = Event.objects.all()
    serializer_class = EventDetailSerializer
    permission_classes = (IsEventHostAdminOrReadOnly|permissions.IsAdminUser,)

    def get(self, request, *args, **kwargs):
        try:
            obj = Event.objects.get(pk=kwargs.get('pk'))
        except Event.DoesNotExist:
            raise Http404
        data = self.retrieve(request, *args, **kwargs).data

        data['event_admin'] = check_is_admin(request.user, obj)
        data['event_registered'] = check_event_registered(request.user, obj)
        return Response(data)


class EventAttendeeList(generics.ListAPIView):
    serializer_class = UserRegisterEventSerializer
    permission_classes = (IsEventRegistered|IsEventHostAdmin|permissions.IsAdminUser, )

    def get_queryset(self):
        try:
            event = Event.objects.get(pk=self.kwargs.get('pk'))
        except Event.DoesNotExist:
            return None
        return UserRegisterEvent.objects.filter(event=event)


class EventAdminList(generics.ListAPIView):
    serializer_class = UserManageEventSerializer
    permission_classes = (IsEventHostAdmin|permissions.IsAdminUser, )

    def get_queryset(self):
        try:
            event = Event.objects.get(pk=self.kwargs.get('pk'))
        except Event.DoesNotExist:
            return None
        return UserManageEvent.objects.filter(event=event)


class TransportCreateView(generics.CreateAPIView):
    # Not Tested

    queryset = Transport.objects.all()
    serializer_class = TransportSerializer
    permission_classes = (IsOwner|IsEventHostAdmin|permissions.IsAdminUser,)

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
    permission_classes = (IsOwner|IsEventHostAdmin|permissions.IsAdminUser,)


class EventCheckInToken(APIView):
    def get(self, request, pk, format=None):
        try:
            event = Event.objects.get(pk=pk)
        except CheckIn.DoesNotExist:
            raise Http404

        if not event.checkin_enabled:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'msg': 'Event Check-in not enabled.'})
        data = {'checkin_token': CheckIn.objects.get(event=event).token}
        return Response(status=status.HTTP_200_OK, data=data)


class UserCheckInEvent(APIView):
    # Not Tested

    permission_classes = (IsOwner|IsEventHostAdmin|permissions.IsAdminUser,)

    def get(self, request, pk, format=None):
        try:
            checkinobj = CheckIn.objects.get(pk=pk)
        except CheckIn.DoesNotExist:
            raise Http404

        event = checkinobj.event
        if not event.checkin_enabled:
            # Should not reach here
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'msg': 'Event Check-in not enabled.'})
        user = request.user
        if 'user_id' in request.data:
            user = get_user_model().objects.get(id=request.data.get('user_id'))

        try:
            ure_obj = UserRegisterEvent.objects.get(user=user, event=event)
        except UserRegisterEvent.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'msg': 'Not registered.'})

        self.check_object_permissions(request, ure_obj)
        if ure_obj.checked_in:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'msg': 'Already checked in.'})
        # ure_obj.checkin()
        # ure_obj.save()
        return Response(status=status.HTTP_200_OK)

    def post(self, request, pk, format=None):
        try:
            checkinobj = CheckIn.objects.get(pk=pk)
        except CheckIn.DoesNotExist:
            raise Http404

        event = checkinobj.event
        if not event.checkin_enabled:
            # Should not reach here
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'msg': 'Event Check-in not enabled.'})
        user = request.user
        if 'user_id' in request.data:
            user = get_user_model().objects.get(id=request.data.get('user_id'))

        try:
            ure_obj = UserRegisterEvent.objects.get(user=user, event=event)
        except UserRegisterEvent.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'msg': 'Not registered.'})

        self.check_object_permissions(request, ure_obj)
        if ure_obj.checked_in:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'msg': 'Already checked in.'})
        ure_obj.checkin()
        ure_obj.save()
        return Response(status=status.HTTP_202_ACCEPTED)


class StartCheckIn(generics.CreateAPIView):
    queryset = CheckIn.objects.all()
    serializer_class = CheckInSerializer
    permission_classes = (IsEventHostAdmin|permissions.IsAdminUser,)

    def perform_create(self, serializer):
        data = self.request.data
        event = Event.objects.get(id=data.get('event_id'))
        if event.checkin_enabled:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'msg': 'Check-in already started.'})
        event.enable_checkin()
        event.save()
        serializer.save(event=event)


class StopCheckIn(generics.DestroyAPIView):
    queryset = CheckIn.objects.all()
    serializer_class = CheckInSerializer
    permission_classes = (IsEventHostAdmin|permissions.IsAdminUser,)

    def perform_destroy(self, instance):
        if instance is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'msg': 'Check-in not started.'})
        event = instance.event
        event.disable_checkin()
        event.save()
        instance.delete()


def index(request):
    return render(request, 'index.html', {})

