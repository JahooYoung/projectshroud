from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.http import Http404, HttpResponse

from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from backend.serializers import *
from backend.permissions import *
from backend.utils.qrcode import text_to_qr
from backend.utils.email import *

from rest_framework.serializers import ValidationError


def check_is_admin(user, event):
    if not isinstance(user, get_user_model()):
        return False
    if user.is_site_admin:
        return True
    return UserManageEvent.objects.filter(user=user, event=event).exists()


def check_is_admin_not_site_admin(user, event):
    return UserManageEvent.objects.filter(user=user, event=event).exists()


def check_event_registered(user, event):
    return UserRegisterEvent.objects.filter(user=user, event=event).exists()


def check_event_register_approved(user, event):
    return UserRegisterEvent.objects.filter(user=user, event=event, approved=True).exists()


@api_view(['POST'])
def github_push(request):
    import pickle
    from django.conf import settings
    with open(os.path.join(settings.BASE_DIR, 'github_push.pk'), 'wb') as f:
        pickle.dump(request.data, f)
    return Response(status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def activate_user(request):
    if 'id' not in request.data:
        raise ValidationError('No id provided.')

    if 'token' not in request.data:
        raise ValidationError('No token provided.')

    try:
        user = get_user_model().objects.get(id=request.data.get('id'))
    except get_user_model().DoesNotExist:
        raise ValidationError('User Not Found.')

    if user.is_activated:
        raise ValidationError('Already activated.')

    if user.activate_token is not None and user.activate_token == request.data.get('token'):
        user.activate()
        return Response(status=status.HTTP_200_OK)

    raise ValidationError('Invalid token.')


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated, IsSiteAdminOrSelf))
def send_activation(request):
    user = request.user
    data = request.GET
    if 'user_id' in data:
        try:
            user = get_user_model().objects.get(id=data.get('user_id'))
        except Event.DoesNotExist:
            raise ValidationError('User Not Found.')

    if user is None or isinstance(user, AnonymousUser):
        raise ValidationError('No User Specified.')
    if user.is_activated:
        raise ValidationError('Already activated.')

    user.generate_activate_token()
    send_activation_email(user)
    return Response(status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def gen_qrcode(request):
    if 'text' not in request.data:
        raise ValidationError('No text provided.')

    text = request.data.get('text')
    qr_img = text_to_qr(text)

    return HttpResponse(qr_img, content_type='image/png')


class DummyView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        content = {
            'status': 'request was permitted',
            'is_activated': request.user.is_activated
        }
        return Response(content)


class UserView(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated, IsActivated, IsSiteAdminOrSelf)


class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.filter(public=True)
    serializer_class = EventListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsActivatedOrReadOnly)

    def perform_create(self, serializer):
        # user = get_user_model().objects.get(id=self.request.data.get('host_id', ''))
        user = self.request.user
        desc = ''

        if 'description' in self.request.data:
            desc = self.request.data.get('description')

        event_obj = serializer.save(host=user, description=desc)

        # done in frontend
        # ume_obj = UserManageEvent(user=user, event=event_obj)
        # ume_obj.save()


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
    permission_classes = (permissions.IsAuthenticated, IsActivated, IsSiteAdminOrSelf)

    def get_queryset(self):
        # user = get_user_model().objects.get(id=self.kwargs.get('pk'))
        user = self.request.user
        return UserRegisterEvent.objects.filter(user=user)


class UserManageEventList(generics.ListAPIView):
    serializer_class = UserManageEventSerializer
    permission_classes = (permissions.IsAuthenticated, IsActivated, IsSiteAdminOrSelf)

    def get_queryset(self):
        # user = get_user_model().objects.get(id=self.kwargs.get('pk'))
        user = self.request.user
        return UserManageEvent.objects.filter(user=user)


class UserRegisterFutureEventList(generics.ListAPIView):
    serializer_class = UserRegisterEventSerializer
    permission_classes = (permissions.IsAuthenticated, IsActivated, IsSiteAdminOrSelf)

    def get_queryset(self):
        # user = get_user_model().objects.get(id=self.kwargs.get('pk'))
        user = self.request.user
        return UserRegisterEvent.objects.filter(user=user, event__start_time__gt=timezone.now())


class UserRegisterPastEventList(generics.ListAPIView):
    serializer_class = UserRegisterEventSerializer
    permission_classes = (permissions.IsAuthenticated, IsActivated, IsSiteAdminOrSelf)

    def get_queryset(self):
        # user = get_user_model().objects.get(id=self.kwargs.get('pk'))
        user = self.request.user
        return UserRegisterEvent.objects.filter(user=user, event__end_time__lte=timezone.now())


class UserRegisterOngoingEventList(generics.ListAPIView):
    serializer_class = UserRegisterEventSerializer
    permission_classes = (permissions.IsAuthenticated, IsActivated, IsSiteAdminOrSelf)

    def get_queryset(self):
        # user = get_user_model().objects.get(id=self.kwargs.get('pk'))
        user = self.request.user
        return UserRegisterEvent.objects.filter(user=user, event__start_time__lte=timezone.now(),
                                                event__end_time__gt=timezone.now())


class UserEventRegister(generics.CreateAPIView):
    serializer_class = UserRegisterEventSerializer
    permission_classes = (permissions.IsAuthenticated, IsActivated)

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
            if check_event_register_approved(user, event):
                raise ValidationError('Already Registered.')
            else:
                raise ValidationError('Already applied, waiting for approval.')

        if event.require_approve:
            if event.require_application:
                if 'application_text' not in data or data.get('application_text') == '':
                    raise ValidationError('Need to provide application info.')
            serializers.save(user=user, event=event, transport=None, approved=False)
            send_registered_email(user, event, approved=True)

        else:
            transport = None
            if 'transport_id' in data:
                try:
                    transport = Transport.objects.get(id=data.get('transport_id'))
                except Event.DoesNotExist:
                    raise ValidationError('Transport Not found.')

            serializer.save(user=user, event=event, transport=transport, approved=True)
            send_registered_email(user, event, approved=True)


class ApproveEventRegister(APIView):
    queryset = UserRegisterEvent.objects.all()
    serializer_class = UserRegisterEventSerializer
    permission_classes = (permissions.IsAuthenticated, IsActivated, IsSiteAdminOrEventManager)

    def post(self, request, format=None):
        data = request.data
        if 'approve' not in data:
            raise ValidationError('Need to provide "approve" (Boolean) field.')

        approve = data['approve']
        if 'user_id' not in data:
            raise ValidationError('No user specified.')
        try:
            user = get_user_model().objects.get(id=data.get('user_id'))
        except get_user_model().DoesNotExist:
            raise ValidationError('User Not Found.')

        event = Event.objects.get(id=data.get('event_id'))

        try:
            ure_obj = UserRegisterEvent.objects.get(user=user, event=event)
        except UserRegisterEvent.DoesNotExist:
            raise ValidationError('Not registered/applied.')

        if approve:
            if ure_obj.approved:
                raise ValidationError('Already Approved.')
            ure_obj.approve()

        if not approve:
            ure_obj.disapprove()
            ure_obj.delete()

        return Response(status=status.HTTP_200_OK)


class UserEventUnregister(APIView):
    queryset = UserRegisterEvent.objects.all()
    serializer_class = UserRegisterEventSerializer
    permission_classes = (permissions.IsAuthenticated, IsActivated, IsSiteAdminOrSelf|IsSiteAdminOrEventManager)

    def post(self, request, format=None):
        user = request.user
        data = request.data
        if 'user_id' in data:
            user = get_user_model().objects.get(id=data.get('user_id'))

        event = Event.objects.get(id=data.get('event_id'))
        if not check_event_registered(user, event):
            raise ValidationError('Not registered.')

        ure_obj = UserRegisterEvent.objects.get(user=user, event=event)
        if ure_obj.transport is not None:
            ure_obj.transport.delete()

        ure_obj.delete()
        return Response(status=status.HTTP_200_OK)


class AssignEventAdmin(generics.CreateAPIView):
    # Not Tested

    serializer_class = UserManageEventSerializer
    permission_classes = (permissions.IsAuthenticated, IsActivated, IsSiteAdminOrEventManager)

    def perform_create(self, serializer):
        user = self.request.user
        data = self.request.data
        if 'user_id' in data:
            try:
                user = get_user_model().objects.get(id=data.get('user_id'))
            except Event.DoesNotExist:
                raise ValidationError('User Not Found.')

        event = Event.objects.get(id=data.get('event_id'))
        if check_is_admin(user, event):
            raise ValidationError('Is admin already.')

        serializer.save(user=user, event=event)


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    # Need More Test

    queryset = Event.objects.all()
    serializer_class = EventDetailSerializer
    permission_classes = (IsEventHostAdminOrReadOnly|IsAdminUser,)

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
    permission_classes = (permissions.IsAuthenticated, IsActivated)

    def get_queryset(self):
        try:
            event = Event.objects.get(pk=self.kwargs.get('pk'))
        except Event.DoesNotExist:
            return None
        if not check_is_admin(self.request.user, event):
            raise ValidationError('Not Authorized.')
        return UserRegisterEvent.objects.filter(event=event)


class EventAdminList(generics.ListAPIView):
    serializer_class = UserManageEventSerializer
    permission_classes = (permissions.IsAuthenticated, IsActivated)

    def get_queryset(self):
        try:
            event = Event.objects.get(pk=self.kwargs.get('pk'))
        except Event.DoesNotExist:
            return None
        if not check_is_admin(self.request.user, event):
            raise ValidationError('Not Authorized.')
        return UserManageEvent.objects.filter(event=event)


class TransportCreateView(generics.CreateAPIView):
    # Not Tested

    queryset = Transport.objects.all()
    serializer_class = TransportSerializer
    permission_classes = (permissions.IsAuthenticated, IsSiteAdminOrSelf|IsSiteAdminOrEventManager)

    def perform_create(self, serializer):
        user = self.request.user
        data = self.request.data
        if 'user_id' in data:
            user = get_user_model().objects.get(id=data['user_id'])

        serializer.save(user=user, event=event)


class TransportView(generics.RetrieveUpdateDestroyAPIView):
    # Not Tested

    queryset = Transport.objects.all()
    serializer_class = TransportSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner|IsEventHostAdmin|IsAdminUser)


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

    permission_classes = (permissions.IsAuthenticated, IsActivated, IsOwner|IsEventHostAdmin|IsAdminUser)

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
    permission_classes = (permissions.IsAuthenticated, IsActivated, IsSiteAdminOrEventManager)

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
    permission_classes = (permissions.IsAuthenticated, IsActivated, IsEventHostAdmin|IsAdminUser)

    def perform_destroy(self, instance):
        if instance is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'msg': 'Check-in not started.'})
        event = instance.event
        event.disable_checkin()
        event.save()
        instance.delete()


def index(request):
    return render(request, 'index.html', {})

